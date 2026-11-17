"""
Phase 6.0 — /explore routes (docs/phase6_route_contracts.md).

Covers the applyAI tests required by letsA(ppl)I's handoff contract §9
and the exit criteria in PHASE_6_OPENING_DECLARATION.md §7.
"""

import copy
import json
import re

import pytest

import app as app_module
import memory.storage as storage
from app import OWNER_COOKIE_NAME, app, get_conversation_state
from memory.storage import load_memory, load_proposals, save_memory
from phase5.bounded_adapter import (
    AUTHORITATIVE_PHRASES,
    CLINICAL_DIAGNOSTIC_TERMS,
    IDENTITY_LOCKING_PHRASES,
)
from phase6.handoff import (
    HandoffValidationError,
    PendingHandoffStore,
    validate_envelope,
)


def make_envelope(**overrides):
    env = {
        "handoff_version": "1.0",
        "handoff_id": "7a1c2e3f-0000-4000-8000-000000000001",
        "source": {
            "system": "letsappli",
            "job_id": "greenhouse:exampleco:42",
            "company": "ExampleCo",
            "title": "Platform Engineer",
            "job_url": "https://boards.example.com/exampleco/jobs/42",
            "interpretation_schema_version": "5.2.0",
            "interpreted_at": "2026-11-10T18:00:00Z",
        },
        "role": {
            "summary_text": "Builds and runs the internal deployment platform.",
            "explicit_requirements": [
                {"requirement_text": "Experience with Kubernetes", "modality": "required"},
                {"requirement_text": "Familiarity with Terraform", "modality": "preferred"},
            ],
            "capability_emphasis": [
                {
                    "domain_label": "Infrastructure automation",
                    "description": "Automating how services are deployed.",
                    "evidence": ["You will own our CI/CD pipelines end to end."],
                },
            ],
            "project_opportunities": [
                {
                    "capability_surface": "Deployment pipeline",
                    "description": "a small service deployed by a pipeline you wrote",
                    "evidence": ["own our CI/CD pipelines"],
                },
            ],
            "structural_notes": "Posting is detailed about tooling and light on team size.",
            "confidence": "HIGH",
        },
        "framing": "This describes what one job posting says. It says nothing about you.",
    }
    for path, value in overrides.items():
        target = env
        keys = path.split(".")
        for k in keys[:-1]:
            target = target[k]
        if value is _DELETE:
            del target[keys[-1]]
        else:
            target[keys[-1]] = value
    return env


_DELETE = object()


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "BASE_MEMORY_DIR", tmp_path)
    monkeypatch.setattr(app_module, "pending_handoffs", PendingHandoffStore())
    return tmp_path


def _owner(client):
    return client.get_cookie(OWNER_COOKIE_NAME).value


def _client():
    c = app.test_client()
    c.get("/")
    return c


def _send(client, envelope):
    """Simulate letsA(ppl)I's cross-site form POST (no cookie is sent)."""
    raw = envelope if isinstance(envelope, str) else json.dumps(envelope)
    stranger = app.test_client()  # cross-site: SameSite=Lax cookie not sent
    return stranger.post("/explore/role", data={"envelope": raw})


def _token(resp):
    assert resp.status_code == 303, resp.data
    m = re.search(r"/explore/role/([^/]+)$", resp.headers["Location"])
    assert m, resp.headers["Location"]
    return m.group(1)


def _send_and_accept(client, envelope=None):
    token = _token(_send(client, envelope or make_envelope()))
    client.get(f"/explore/role/{token}")
    resp = client.post(f"/explore/role/{token}/accept")
    assert resp.status_code == 303
    return token


def _role(client):
    return get_conversation_state(_owner(client))["role_context"]


# ------------------------------------------------------------
# Intake: POST /explore/role
# ------------------------------------------------------------

def test_valid_envelope_is_parked_and_redirects_to_preview():
    resp = _send(None, make_envelope())
    token = _token(resp)
    assert len(app_module.pending_handoffs) == 1
    assert app_module.pending_handoffs.peek(token)["source"]["title"] == "Platform Engineer"


@pytest.mark.parametrize("overrides, reason", [
    ({"handoff_version": "2.0"}, "handoff_version"),
    ({"handoff_version": "1"}, "handoff_version"),
    ({"source.system": "someone-else"}, "source.system"),
    ({"source.job_url": "http://boards.example.com/42"}, "https"),
    ({"source.job_url": "javascript:alert(1)"}, "https"),
    ({"source.interpreted_at": "yesterday"}, "ISO-8601"),
    ({"role.confidence": "CERTAIN"}, "confidence"),
    ({"role.capability_emphasis": []}, "capability_emphasis"),
    ({"role.explicit_requirements": [{"requirement_text": "x", "modality": "must"}]}, "modality"),
    ({"framing": _DELETE}, "missing"),
    ({"role.summary_text": "   "}, "empty"),
])
def test_invalid_envelopes_are_rejected_and_nothing_is_parked(overrides, reason):
    resp = _send(None, make_envelope(**overrides))
    assert resp.status_code == 400
    assert reason in resp.data.decode("utf-8")
    assert len(app_module.pending_handoffs) == 0


@pytest.mark.parametrize("where", ["", "source.", "role.", "role.capability_emphasis.0."])
def test_unknown_keys_are_rejected_at_every_level(where):
    env = make_envelope()
    target = env
    for k in [k for k in where.split(".") if k]:
        target = target[int(k)] if k.isdigit() else target[k]
    target["fit_score"] = 0.9

    resp = _send(None, env)

    assert resp.status_code == 400
    assert "unknown keys: fit_score" in resp.data.decode("utf-8")
    assert len(app_module.pending_handoffs) == 0


def test_excluded_letsappli_fields_are_rejected():
    env = make_envelope()
    env["role"]["implicit_signals"] = [{"signal_text": "fast-paced"}]
    assert _send(None, env).status_code == 400

    env = make_envelope()
    env["source"]["pipeline_status"] = "applied"
    assert _send(None, env).status_code == 400


def test_non_json_and_missing_envelope_are_rejected():
    assert _send(None, "not json").status_code == 400
    assert app.test_client().post("/explore/role", data={}).status_code == 400
    assert len(app_module.pending_handoffs) == 0


def test_oversize_envelope_is_413():
    env = make_envelope()
    env["role"]["structural_notes"] = "x" * 70_000
    resp = _send(None, env)
    assert resp.status_code == 413
    assert len(app_module.pending_handoffs) == 0


def test_validator_returns_only_allowlisted_fields():
    clean = validate_envelope(make_envelope())
    assert set(clean) == {"handoff_version", "handoff_id", "source", "role", "framing"}
    with pytest.raises(HandoffValidationError):
        validate_envelope(["not", "an", "object"])


def test_intake_logs_only_handoff_id_and_received_at(monkeypatch):
    events = []
    monkeypatch.setattr(app_module.logger, "event", lambda **kw: events.append(kw))

    _send(None, make_envelope())

    [event] = [e for e in events if e["event_type"] == "phase6.handoff_received"]
    assert set(event["payload"]) == {"handoff_id", "received_at"}
    assert "Platform Engineer" not in json.dumps(events)


# ------------------------------------------------------------
# Preview, accept, discard
# ------------------------------------------------------------

def test_viewing_preview_binds_nothing_and_keeps_token():
    client = _client()
    token = _token(_send(client, make_envelope()))

    page = client.get(f"/explore/role/{token}")

    assert page.status_code == 200
    html = page.data.decode("utf-8")
    assert "Platform Engineer" in html
    assert "Explore this role" in html
    assert "It says nothing about you." in html
    assert _role(client) is None
    assert app_module.pending_handoffs.peek(token) is not None


def test_accept_binds_role_to_accepting_owner_only():
    alice = _client()
    bob = _client()

    _send_and_accept(alice)

    assert _role(alice)["source"]["title"] == "Platform Engineer"
    assert _role(bob) is None


def test_token_is_single_use():
    alice = _client()
    bob = _client()
    token = _send_and_accept(alice)

    again = bob.post(f"/explore/role/{token}/accept")

    assert again.status_code == 404
    assert "send it again from letsA(ppl)I" in again.data.decode("utf-8")
    assert _role(bob) is None
    assert bob.get(f"/explore/role/{token}").status_code == 404


def test_unknown_token_is_404():
    client = _client()
    assert client.get("/explore/role/not-a-token").status_code == 404
    assert client.post("/explore/role/not-a-token/accept").status_code == 404


def test_expired_token_is_rejected(monkeypatch):
    now = [1000.0]
    monkeypatch.setattr(app_module, "pending_handoffs", PendingHandoffStore(clock=lambda: now[0]))
    client = _client()
    token = _token(_send(client, make_envelope()))

    now[0] += 5 * 60 + 1

    assert client.get(f"/explore/role/{token}").status_code == 404
    assert client.post(f"/explore/role/{token}/accept").status_code == 404
    assert _role(client) is None


def test_discard_drops_token_without_binding():
    client = _client()
    token = _token(_send(client, make_envelope()))

    resp = client.post(f"/explore/role/{token}/discard")

    assert resp.status_code == 303
    assert app_module.pending_handoffs.peek(token) is None
    assert _role(client) is None
    assert client.post(f"/explore/role/{token}/discard").status_code == 303  # idempotent


def test_pending_store_is_bounded():
    store = PendingHandoffStore(max_pending=3)
    tokens = [store.park({"n": i}) for i in range(5)]
    assert len(store) == 3
    assert store.peek(tokens[0]) is None
    assert store.peek(tokens[4]) == {"n": 4}


def test_new_accept_replaces_previous_role():
    client = _client()
    _send_and_accept(client)
    _send_and_accept(client, make_envelope(**{"source.title": "Data Engineer"}))
    assert _role(client)["source"]["title"] == "Data Engineer"


# ------------------------------------------------------------
# /explore (Path A walkthrough)
# ------------------------------------------------------------

def test_explore_without_role_explains_how_roles_arrive():
    html = _client().get("/explore").data.decode("utf-8")
    assert "No role is loaded" in html


def test_explore_shows_role_projects_limits_and_banner_in_order():
    client = _client()
    env = make_envelope()
    env["role"]["project_opportunities"].append({
        "capability_surface": "Second surface",
        "description": "a second idea",
        "evidence": ["second quote"],
    })
    _send_and_accept(client, env)

    html = client.get("/explore").data.decode("utf-8")

    assert "Exploring a role:" in html
    assert "Clear role context" in html
    assert "It says nothing about you." in html
    assert "Experience with Kubernetes" in html
    assert "One way to show this would be: a small service deployed by a pipeline you wrote" in html
    assert "No project guarantees an interview, an offer, or any outcome." in html
    assert html.index("Deployment pipeline") < html.index("Second surface")  # envelope order


def test_explore_escapes_envelope_html():
    client = _client()
    _send_and_accept(client, make_envelope(**{"role.summary_text": "<script>alert('x')</script>"}))

    html = client.get("/explore").data.decode("utf-8")

    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html


def test_explore_shows_memory_only_when_selected_and_separately(isolated):
    client = _client()
    owner = _owner(client)
    save_memory(owner, [{
        "id": "m1",
        "owner_id": owner,
        "text": "I enjoy untangling build systems.",
        "kind": "SELF_OBSERVATION",
        "source": {"source_type": "phase3_reflection"},
        "created_at": "2026-11-01T00:00:00+00:00",
        "updated_at": "2026-11-01T00:00:00+00:00",
        "status": "active",
        "deleted_at": None,
    }])
    _send_and_accept(client)

    before = client.get("/explore").data.decode("utf-8")
    assert "I enjoy untangling build systems." not in before
    assert "No memory is being used" in before

    client.post("/memory/select", data={"memory_id": ["m1"]})
    after = client.get("/explore").data.decode("utf-8")

    assert "Using the items you selected" in after
    materials = after[after.index("Your selected materials"):]
    assert "I enjoy untangling build systems." in materials
    role_part = after[:after.index("Your selected materials")]
    assert "I enjoy untangling build systems." not in role_part


# ------------------------------------------------------------
# Language guard (declaration §4 invariants 1–4)
# ------------------------------------------------------------

FORBIDDEN_PHASE6_PHRASES = [
    "fit", "match", "score", "ready", "readiness", "missing", "good at",
    "qualified", "recommend", "best", "guaranteed", "will get",
]


def _visible_text(html):
    return re.sub(r"<[^>]+>", " ", html)


@pytest.mark.parametrize("path_kind", ["preview", "explore", "explore_empty", "expired"])
def test_phase6_pages_use_no_fit_identity_or_authority_language(path_kind):
    client = _client()
    if path_kind == "preview":
        token = _token(_send(client, make_envelope()))
        html = client.get(f"/explore/role/{token}").data.decode("utf-8")
    elif path_kind == "explore":
        _send_and_accept(client)
        html = client.get("/explore").data.decode("utf-8")
    elif path_kind == "explore_empty":
        html = client.get("/explore").data.decode("utf-8")
    else:
        html = client.get("/explore/role/nope").data.decode("utf-8")

    text = _visible_text(html).lower()
    # Remove the fixture's own posting text so only our copy is checked.
    for s in [
        "builds and runs the internal deployment platform.",
        "posting is detailed about tooling and light on team size.",
    ]:
        text = text.replace(s, "")

    for phrase in FORBIDDEN_PHASE6_PHRASES:
        assert not re.search(rf"\b{re.escape(phrase)}\b", text), phrase
    for phrase in IDENTITY_LOCKING_PHRASES + AUTHORITATIVE_PHRASES:
        assert phrase not in text, phrase
    for term in CLINICAL_DIAGNOSTIC_TERMS:
        assert not re.search(rf"\b{re.escape(term)}\b", text), term


# ------------------------------------------------------------
# Leaving the mode, and no writes
# ------------------------------------------------------------

def test_clear_role_context_keeps_everything_else():
    client = _client()
    owner = _owner(client)
    client.post("/", data={"user_input": "I would sketch a few screens first."})
    client.post("/memory/select", data={"memory_id": []})
    _send_and_accept(client)
    state_before = dict(get_conversation_state(owner))

    resp = client.post("/explore/role/clear")

    state = get_conversation_state(owner)
    assert resp.status_code == 303
    assert state["role_context"] is None
    assert state["responses"] == state_before["responses"]
    assert state["stage"] == state_before["stage"]
    assert state["session_id"] == state_before["session_id"]


def test_reset_clears_role_context():
    client = _client()
    _send_and_accept(client)
    client.get("/reset")
    assert _role(client) is None


def test_phase6_writes_nothing_to_memory_proposals_or_disk(isolated):
    client = _client()
    owner = _owner(client)
    token = _token(_send(client, make_envelope()))
    client.get(f"/explore/role/{token}")
    client.post(f"/explore/role/{token}/accept")
    client.get("/explore")
    client.post("/explore/role/clear")

    assert load_memory(owner) == []
    assert load_proposals(owner) == []
    assert list(isolated.rglob("*")) == []


def test_role_context_is_per_owner_and_not_shared_by_reference():
    alice = _client()
    bob = _client()
    env = make_envelope()
    _send_and_accept(alice, env)
    _send_and_accept(bob, copy.deepcopy(env))

    alice.post("/explore/role/clear")

    assert _role(alice) is None
    assert _role(bob)["source"]["title"] == "Platform Engineer"
