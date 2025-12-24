from phase5.boundary import LLMBoundary
from phase5.null_adapter import NullLLMAdapter
from phase5.request import LLMRequest
from phase5.roles import ParticipantRole, IntelligenceMode


def base_request(**overrides):
    data = {
        "user_text": "test input",
        "role": ParticipantRole.OBSERVER,
        "intelligence_mode": IntelligenceMode.NONE,
        "consent_token": None,
        "disallowed_capabilities": ["recommendation", "diagnosis"],
    }
    data.update(overrides)
    return LLMRequest(**data)


def test_boundary_denies_invalid_request_before_adapter():
    boundary = LLMBoundary(adapter=NullLLMAdapter())

    request = base_request(
        intelligence_mode=IntelligenceMode.SHALLOW,
        consent_token=None
    )

    response = boundary.evaluate(request)

    assert response.status == "denied"
    assert "consent" in response.message.lower()


def test_boundary_allows_valid_request_to_adapter():
    boundary = LLMBoundary(adapter=NullLLMAdapter())

    request = base_request(
        intelligence_mode=IntelligenceMode.NONE
    )

    response = boundary.evaluate(request)

    assert response.status == "no_intelligence"
    assert response.content is None


def test_null_adapter_never_returns_content():
    boundary = LLMBoundary(adapter=NullLLMAdapter())

    request = base_request(
        intelligence_mode=IntelligenceMode.NONE
    )

    response = boundary.evaluate(request)

    assert response.content is None
def test_consent_revocation_denies_phase5_afterward():
    boundary = LLMBoundary(adapter=NullLLMAdapter())

    # Step 1: Consent is present → request would be allowed by policy
    request_with_consent = base_request(
        intelligence_mode=IntelligenceMode.SHALLOW,
        consent_token="phase5_session"
    )

    response_allowed = boundary.evaluate(request_with_consent)

    # Even though the adapter is null, the request passes policy
    assert response_allowed.status != "denied"

    # Step 2: Consent is revoked → same request should now be denied
    request_after_revocation = base_request(
        intelligence_mode=IntelligenceMode.SHALLOW,
        consent_token=None
    )

    response_denied = boundary.evaluate(request_after_revocation)

    assert response_denied.status == "denied"
    assert "consent" in response_denied.message.lower()
