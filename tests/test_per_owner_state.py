"""
Per-owner conversation state isolation.

Each owner (ce_owner_id cookie) must get an isolated conversation.
One owner's answers, feedback, or reset must never be visible to,
or change, another owner's conversation.

These tests stay in stage 1 so no summary runs and no memory
proposals are written to disk.
"""

import pytest

import app as app_module
from app import (
    OWNER_COOKIE_NAME,
    QUESTIONS,
    app,
    get_conversation_state,
    reset_conversation_state,
)


NEUTRAL_ANSWER = "I would sketch a few screens and test them with friends."


def _owner_id(client) -> str:
    cookie = client.get_cookie(OWNER_COOKIE_NAME)
    assert cookie is not None, "Expected the owner cookie to be set"
    return cookie.value


@pytest.fixture
def two_owners():
    a = app.test_client()
    b = app.test_client()
    a.get("/")
    b.get("/")
    return a, b


def test_each_client_gets_a_distinct_owner_and_session(two_owners):
    a, b = two_owners
    owner_a, owner_b = _owner_id(a), _owner_id(b)

    assert owner_a != owner_b

    state_a = get_conversation_state(owner_a)
    state_b = get_conversation_state(owner_b)
    assert state_a is not state_b
    assert state_a["session_id"] != state_b["session_id"]
    assert state_a["owner_id"] == owner_a
    assert state_b["owner_id"] == owner_b


def test_answers_do_not_leak_between_owners(two_owners):
    a, b = two_owners

    a.post("/", data={"user_input": NEUTRAL_ANSWER})

    state_a = get_conversation_state(_owner_id(a))
    state_b = get_conversation_state(_owner_id(b))

    assert state_a["responses"].get(1) == NEUTRAL_ANSWER
    assert state_b["responses"] == {}
    assert state_b["stage"] == 1
    assert all(e["content"] != NEUTRAL_ANSWER for e in state_b["conversation_log"])

    # B still sees the first question, not wherever A is.
    page_b = b.get("/").data.decode("utf-8")
    assert NEUTRAL_ANSWER not in page_b


def test_feedback_is_scoped_to_its_owner(two_owners):
    a, b = two_owners

    a.post("/feedback", data={"feedback": "yes", "feedback_detail": "from A"})

    assert get_conversation_state(_owner_id(a))["feedback"]["detail"] == "from A"
    assert get_conversation_state(_owner_id(b))["feedback"]["detail"] == "..."


def test_reset_only_affects_its_owner(two_owners):
    a, b = two_owners
    a.post("/", data={"user_input": NEUTRAL_ANSWER})
    b.post("/", data={"user_input": NEUTRAL_ANSWER})

    old_session_a = get_conversation_state(_owner_id(a))["session_id"]

    a.get("/reset")

    state_a = get_conversation_state(_owner_id(a))
    state_b = get_conversation_state(_owner_id(b))

    assert state_a["responses"] == {}
    assert state_a["stage"] == 1
    assert state_a["session_id"] != old_session_a
    assert state_b["responses"].get(1) == NEUTRAL_ANSWER


def test_returning_owner_resumes_own_conversation(two_owners):
    a, _ = two_owners
    a.post("/", data={"user_input": NEUTRAL_ANSWER})
    stage_after_answer = get_conversation_state(_owner_id(a))["stage"]

    a.get("/")

    assert get_conversation_state(_owner_id(a))["stage"] == stage_after_answer


def test_request_without_cookie_does_not_reuse_existing_state(two_owners):
    a, _ = two_owners
    a.post("/", data={"user_input": NEUTRAL_ANSWER})

    stranger = app.test_client()
    page = stranger.get("/").data.decode("utf-8")

    assert NEUTRAL_ANSWER not in page
    assert get_conversation_state(_owner_id(stranger))["responses"] == {}


def test_new_and_reset_states_keep_existing_consent_defaults():
    # Behavior preserved from the old global state: a fresh conversation
    # starts with the dev consent token, a reset one starts with None.
    fresh = get_conversation_state("owner-consent-defaults")
    assert fresh["phase5_consent_token"] == app_module.INITIAL_PHASE5_CONSENT_TOKEN

    reset = reset_conversation_state("owner-consent-defaults")
    assert reset["phase5_consent_token"] is None


@pytest.mark.parametrize("bad_owner", ["", None])
def test_state_requires_owner_id(bad_owner):
    with pytest.raises(ValueError):
        get_conversation_state(bad_owner)
    with pytest.raises(ValueError):
        reset_conversation_state(bad_owner)


def test_first_question_is_shown_to_new_owner():
    client = app.test_client()
    page = client.get("/").data.decode("utf-8")
    first_line = QUESTIONS[1].split("\n")[0]
    # Jinja escapes apostrophes; compare on a safe prefix.
    assert first_line[:30] in page
