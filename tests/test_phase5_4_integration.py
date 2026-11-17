"""
Phase 5.4 — integration tests over the real Flask routes.

Covers the checklist items that the primitive-level tests in
test_phase5_4_memory.py do not:

* opt-in gating (no proposals unless the user asks) and separation
  from Phase 5 consent
* phase ordering (proposals only after the summary)
* approve writes correct, server-generated timestamps through the store
* forget (route + non-use)
* cross-owner isolation
* persistence across restarts, including legacy v0 records
* selection: memory reaches downstream use only when selected, with attribution

All file I/O is redirected to a temp directory.
"""

import json

import pytest

import app as app_module
import memory.storage as storage
from app import OWNER_COOKIE_NAME, app, build_selected_memory_context, get_conversation_state
from memory.file_store import FileBackedMemoryStore
from memory.storage import load_memory, load_proposals, save_memory, save_proposals
from test_answers import TEST_RESPONSES


@pytest.fixture(autouse=True)
def isolated_memory_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "BASE_MEMORY_DIR", tmp_path)
    return tmp_path


def _owner(client) -> str:
    return client.get_cookie(OWNER_COOKIE_NAME).value


def _new_client():
    client = app.test_client()
    client.get("/")
    return client


def _drive_to_summary(client):
    page = None
    for answer in TEST_RESPONSES.values():
        page = client.post("/", data={"user_input": answer})
    state = get_conversation_state(_owner(client))
    assert state["summary_ready"], "Test answers should reach the summary"
    assert state["summary_reflections"], "Test answers should produce reflections"
    return page


def _opt_in_and_approve_first(client) -> dict:
    client.post("/memory/opt-in")
    pending = [p for p in load_proposals(_owner(client)) if p["decision"] == "pending"]
    client.post(f"/memory/proposals/{pending[0]['proposal_id']}/approve")
    memory = load_memory(_owner(client))
    assert len(memory) == 1
    return memory[0]


# ------------------------------------------------------------
# Opt-in gating and phase ordering
# ------------------------------------------------------------

def test_summary_alone_creates_no_proposals_and_offers_opt_in():
    client = _new_client()
    page = _drive_to_summary(client).data.decode("utf-8")

    assert load_proposals(_owner(client)) == []
    assert load_memory(_owner(client)) == []
    assert "/memory/opt-in" in page


def test_opt_in_before_summary_is_rejected():
    client = _new_client()
    client.post("/", data={"user_input": TEST_RESPONSES[1]})

    resp = client.post("/memory/opt-in")

    assert resp.status_code == 409
    assert load_proposals(_owner(client)) == []


def test_opt_in_after_summary_creates_pending_proposals_only_once():
    client = _new_client()
    _drive_to_summary(client)
    reflections = get_conversation_state(_owner(client))["summary_reflections"]

    client.post("/memory/opt-in")
    client.post("/memory/opt-in")  # replay

    proposals = load_proposals(_owner(client))
    assert [p["proposed_text"] for p in proposals] == reflections
    assert all(p["decision"] == "pending" for p in proposals)
    assert all(p["kind"] == "SELF_OBSERVATION" for p in proposals)
    assert load_memory(_owner(client)) == []


def test_memory_opt_in_is_separate_from_phase5_consent():
    client = _new_client()
    _drive_to_summary(client)
    client.post("/memory/opt-in")

    state = get_conversation_state(_owner(client))
    assert state["memory_opt_in"] is True
    assert state["phase5_consent_token"] is None


def test_phase5_consent_offer_does_not_create_proposals():
    client = _new_client()
    client.post("/", data={"user_input": "Can you analyze this pattern?"})

    state = get_conversation_state(_owner(client))
    assert state["phase5_offer_shown"] is True
    assert state["memory_opt_in"] is False
    assert load_proposals(_owner(client)) == []


# ------------------------------------------------------------
# Approve
# ------------------------------------------------------------

def test_approve_writes_iso_timestamps_and_source_through_store():
    client = _new_client()
    _drive_to_summary(client)
    item = _opt_in_and_approve_first(client)

    assert isinstance(item["created_at"], str)
    assert item["created_at"] == item["updated_at"]
    assert item["kind"] == "SELF_OBSERVATION"
    assert item["source"] == {"source_type": "phase3_reflection"}
    assert item["status"] == "active"

    listed = FileBackedMemoryStore().list(_owner(client))
    assert listed[0].created_at is not None
    assert listed[0].created_at.isoformat() == item["created_at"]


def test_approve_rejects_identity_locking_text_and_keeps_proposal_pending():
    client = _new_client()
    owner = _owner(client)
    save_proposals(owner, [{
        "proposal_id": "1",
        "owner_id": owner,
        "proposed_text": "You are a natural leader.",
        "kind": "SELF_OBSERVATION",
        "source_type": "phase3_reflection",
        "decision": "pending",
        "created_at": None,
    }])

    resp = client.post("/memory/proposals/1/approve")

    assert resp.status_code == 400
    assert load_memory(owner) == []
    assert load_proposals(owner)[0]["decision"] == "pending"


def test_approve_rejects_kind_outside_allowlist():
    client = _new_client()
    owner = _owner(client)
    save_proposals(owner, [{
        "proposal_id": "1",
        "owner_id": owner,
        "proposed_text": "I like mornings.",
        "kind": "TRAIT",
        "source_type": "phase3_reflection",
        "decision": "pending",
        "created_at": None,
    }])

    resp = client.post("/memory/proposals/1/approve")

    assert resp.status_code == 400
    assert load_memory(owner) == []


def test_decline_does_not_retain_proposal_text():
    client = _new_client()
    _drive_to_summary(client)
    client.post("/memory/opt-in")
    first = load_proposals(_owner(client))[0]

    client.post(f"/memory/proposals/{first['proposal_id']}/decline")

    declined = next(p for p in load_proposals(_owner(client)) if p["proposal_id"] == first["proposal_id"])
    assert declined["decision"] == "declined"
    assert declined["proposed_text"] == ""
    assert first["proposed_text"] not in json.dumps(load_proposals(_owner(client)))
    assert load_memory(_owner(client)) == []


# ------------------------------------------------------------
# Forget
# ------------------------------------------------------------

def test_forget_removes_item_from_ledger_and_soft_deletes():
    client = _new_client()
    _drive_to_summary(client)
    item = _opt_in_and_approve_first(client)

    assert item["text"] in client.get("/memory").data.decode("utf-8")

    resp = client.post(f"/memory/{item['id']}/forget")
    assert resp.status_code == 302

    assert item["text"] not in client.get("/memory").data.decode("utf-8")
    raw = load_memory(_owner(client))
    assert raw[0]["status"] == "deleted"
    assert raw[0]["deleted_at"] is not None
    assert FileBackedMemoryStore().list(_owner(client)) == []


def test_forget_is_idempotent_and_unknown_id_is_404():
    client = _new_client()
    _drive_to_summary(client)
    item = _opt_in_and_approve_first(client)

    client.post(f"/memory/{item['id']}/forget")
    again = client.post(f"/memory/{item['id']}/forget")

    assert again.status_code == 302
    assert client.post("/memory/does-not-exist/forget").status_code == 404


def test_reset_keeps_memory():
    client = _new_client()
    _drive_to_summary(client)
    item = _opt_in_and_approve_first(client)

    client.get("/reset")

    assert [i.id for i in FileBackedMemoryStore().list(_owner(client))] == [item["id"]]


# ------------------------------------------------------------
# Cross-owner isolation
# ------------------------------------------------------------

def test_other_owner_cannot_see_forget_approve_or_select_my_memory():
    alice = _new_client()
    _drive_to_summary(alice)
    item = _opt_in_and_approve_first(alice)
    alice.post("/memory/opt-in")
    alice_pending = [p for p in load_proposals(_owner(alice)) if p["decision"] == "pending"]

    bob = _new_client()

    assert item["text"] not in bob.get("/memory").data.decode("utf-8")
    assert bob.post(f"/memory/{item['id']}/forget").status_code == 404
    if alice_pending:
        pid = alice_pending[0]["proposal_id"]
        assert bob.post(f"/memory/proposals/{pid}/approve").status_code == 404
        assert bob.post(f"/memory/proposals/{pid}/decline").status_code == 404

    bob.post("/memory/select", data={"memory_id": [item["id"]]})
    assert get_conversation_state(_owner(bob))["selected_memory_ids"] == []

    # Alice is untouched.
    assert load_memory(_owner(alice))[0]["status"] == "active"
    assert load_memory(_owner(bob)) == []


# ------------------------------------------------------------
# Persistence across restarts
# ------------------------------------------------------------

def test_memory_survives_restart_and_deletion_persists(monkeypatch):
    client = _new_client()
    _drive_to_summary(client)
    item = _opt_in_and_approve_first(client)
    owner = _owner(client)

    # Simulate a restart: all in-process state is gone.
    monkeypatch.setattr(app_module, "_conversation_states", {})

    assert [i.id for i in FileBackedMemoryStore().list(owner)] == [item["id"]]
    assert item["text"] in client.get("/memory").data.decode("utf-8")

    client.post(f"/memory/{item['id']}/forget")
    monkeypatch.setattr(app_module, "_conversation_states", {})

    assert FileBackedMemoryStore().list(owner) == []
    assert FileBackedMemoryStore().get(owner, item["id"], include_deleted=True).status == "deleted"


def test_legacy_v0_records_are_read_with_their_real_timestamps():
    owner = "legacy-owner"
    save_memory(owner, [{
        "id": "old-1",
        "owner_id": owner,
        "text": "I prefer sketching before building.",
        "kind": "SELF_OBSERVATION",
        "source_type": "phase3_reflection",
        "status": "active",
        "created_at": 1767000000.0,
        "updated_at": 1767000000.0,
    }])

    [item] = FileBackedMemoryStore().list(owner)

    assert item.created_at.timestamp() == 1767000000.0
    assert item.source.source_type == "phase3_reflection"


# ------------------------------------------------------------
# Selection (the only path to downstream use)
# ------------------------------------------------------------

def test_no_memory_is_used_until_selected():
    client = _new_client()
    _drive_to_summary(client)
    _opt_in_and_approve_first(client)

    context = build_selected_memory_context(_owner(client), get_conversation_state(_owner(client)))

    assert context.resolved_texts == []
    assert context.attribution_line == ""
    assert "No memory is being used" in client.get("/memory/select").data.decode("utf-8")


def test_selected_memory_is_used_with_attribution():
    client = _new_client()
    _drive_to_summary(client)
    item = _opt_in_and_approve_first(client)

    client.post("/memory/select", data={"memory_id": [item["id"], "bogus-id"]})
    state = get_conversation_state(_owner(client))
    context = build_selected_memory_context(_owner(client), state)

    assert state["selected_memory_ids"] == [item["id"]]
    assert context.resolved_texts == [item["text"]]
    assert context.attribution_line == "Using the items you selected…"
    assert "Using the items you selected" in client.get("/memory/select").data.decode("utf-8")


def test_selection_is_cleared_by_clear_forget_and_reset_and_never_persisted(isolated_memory_dir):
    client = _new_client()
    _drive_to_summary(client)
    item = _opt_in_and_approve_first(client)
    owner = _owner(client)

    client.post("/memory/select", data={"memory_id": [item["id"]]})
    on_disk = json.dumps([p.read_text() for p in isolated_memory_dir.rglob("*.json")])
    assert "selected_memory_ids" not in on_disk

    client.post("/memory/select/clear")
    assert get_conversation_state(owner)["selected_memory_ids"] == []

    client.post("/memory/select", data={"memory_id": [item["id"]]})
    client.get("/reset")
    assert get_conversation_state(owner)["selected_memory_ids"] == []

    client.post("/memory/select", data={"memory_id": [item["id"]]})
    client.post(f"/memory/{item['id']}/forget")
    assert get_conversation_state(owner)["selected_memory_ids"] == []
    assert build_selected_memory_context(owner, get_conversation_state(owner)).resolved_texts == []
