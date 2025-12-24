import pytest

from phase5.request import LLMRequest
from phase5.roles import ParticipantRole, IntelligenceMode
from phase5.policy import validate_llm_request


def base_request(**overrides):
    """
    Helper to create a minimal valid request,
    overridden per test.
    """
    data = {
        "user_text": "test input",
        "role": ParticipantRole.OBSERVER,
        "intelligence_mode": IntelligenceMode.NONE,
        "consent_token": None,
        "disallowed_capabilities": ["recommendation", "diagnosis"],
    }
    data.update(overrides)
    return LLMRequest(**data)


def test_none_mode_does_not_require_consent():
    request = base_request(
        intelligence_mode=IntelligenceMode.NONE,
        consent_token=None
    )

    allowed, reason = validate_llm_request(request)

    assert allowed is True
    assert reason is None


def test_shallow_mode_without_consent_is_denied():
    request = base_request(
        intelligence_mode=IntelligenceMode.SHALLOW,
        consent_token=None
    )

    allowed, reason = validate_llm_request(request)

    assert allowed is False
    assert "consent" in reason.lower()


def test_deliberative_mode_without_consent_is_denied():
    request = base_request(
        intelligence_mode=IntelligenceMode.DELIBERATIVE,
        consent_token=None
    )

    allowed, reason = validate_llm_request(request)

    assert allowed is False
    assert "consent" in reason.lower()


def test_missing_recommendation_block_is_denied():
    request = base_request(
        intelligence_mode=IntelligenceMode.SHALLOW,
        consent_token="user-consented",
        disallowed_capabilities=["diagnosis"]  # missing "recommendation"
    )

    allowed, reason = validate_llm_request(request)

    assert allowed is False
    assert "recommendation" in reason.lower()


def test_valid_shallow_request_is_allowed():
    request = base_request(
        intelligence_mode=IntelligenceMode.SHALLOW,
        consent_token="user-consented",
        disallowed_capabilities=["recommendation", "diagnosis"]
    )

    allowed, reason = validate_llm_request(request)

    assert allowed is True
    assert reason is None
