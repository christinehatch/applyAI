import pytest

"""
Phase 5.3 — Bounded Analytical Participation
Acceptance tests for interaction flow only.

These tests intentionally FAIL or SKIP.
They define the contract before implementation.
"""


# ------------------------------------------------------------
# FIXTURE PLACEHOLDERS
# ------------------------------------------------------------

@pytest.fixture
def conversation_state():
    """
    Placeholder fixture representing a conversation
    that has completed Phases 1–3 and is eligible for Phase 5.3.
    """
    return {
        "stage": "post_summary",
        "signals_visible": ["support_seeking", "systems_thinking"],
        "phase5_consent_token": "dev-consent",
        "phase5_3_enabled": False,
    }


@pytest.fixture
def user_request_interpretation():
    """
    User explicitly asks for interpretation.
    """
    return "What does this say about how I think?"


# ------------------------------------------------------------
# PHASE 5.3 ENTRY CONDITIONS
# ------------------------------------------------------------

def test_phase5_3_not_triggered_without_explicit_request():
    """
    The system must NEVER enter Phase 5.3 implicitly.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    request = LLMRequest(
        user_text="I answered the questions already.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.BOUNDED,
        consent_token="user-consented",
        disallowed_capabilities=["recommendation", "diagnosis"],
        phase_context={
            "phase3_complete": True,
            "stage": "post_summary"
        }
    )

    response = boundary.evaluate(request)

    # 🔒 Assert silent refusal (no Phase 5.3 activation)
    assert response.status in ("ignored", "noop", "denied")
    assert response.content is None


def test_phase5_3_requires_prior_phases_completed():
    """
    Phase 5.3 must not be available before Phase 3 reflection.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    request = LLMRequest(
        user_text="Please analyze my answers.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.BOUNDED,
        consent_token="user-consented",
        disallowed_capabilities=["recommendation", "diagnosis"],
        phase_context={
            "phase3_complete": False,   # 🔴 not complete
            "stage": "post_summary"
        }
    )

    response = boundary.evaluate(request)

    # 🔒 Must refuse due to phase ordering
    assert response.status == "denied"
    assert "phase 3" in response.message.lower()

def test_phase5_3_requires_consent_token():
    """
    Phase 5.3 must hard-fail without consent.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    request = LLMRequest(
        user_text="Please analyze my answers.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.BOUNDED,
        consent_token=None,  # 🔴 missing consent
        disallowed_capabilities=["recommendation", "diagnosis"],
        phase_context={
            "phase3_complete": True,
            "stage": "post_summary"
        }
    )

    response = boundary.evaluate(request)

    assert response.status == "denied"
    assert "consent" in response.message.lower()


# ------------------------------------------------------------
# INTERPRETATION OFFER
# ------------------------------------------------------------

def test_system_offers_multiple_interpretations_not_single_answer():
    """
    The system must offer multiple possible interpretations,
    not a single authoritative explanation.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    request = LLMRequest(
        user_text="Please analyze my answers and suggest interpretations.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.BOUNDED,
        consent_token="user-consented",
        disallowed_capabilities=["recommendation", "diagnosis"],
        phase_context={
            "phase3_complete": True,
            "stage": "post_summary"
        }
    )

    response = boundary.evaluate(request)

    assert response.status == "awaiting_resonance"
    assert isinstance(response.content, list)
    assert len(response.content) >= 2


def test_interpretations_are_clearly_labeled_as_optional():
    """
    Interpretation language must explicitly signal uncertainty.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    request = LLMRequest(
        user_text="Please analyze my answers and offer interpretations.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.BOUNDED,
        consent_token="user-consented",
        disallowed_capabilities=["recommendation", "diagnosis"],
        phase_context={
            "phase3_complete": True,
            "stage": "post_summary"
        }
    )

    response = boundary.evaluate(request)

    assert response.status == "awaiting_resonance"
    assert isinstance(response.content, list)

    uncertainty_markers = [
        "possible",
        "could",
        "might",
        "one way to",
        "another interpretation",
        "may suggest"
    ]

    for interpretation in response.content:
        lowered = interpretation.lower()
        assert any(
            marker in lowered for marker in uncertainty_markers
        ), f"Missing uncertainty framing: {interpretation}"



def test_user_must_choose_resonance_or_reject():
    """
    The user must be prompted to choose how (or if)
    the interpretations resonate.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    request = LLMRequest(
        user_text="Please analyze my answers and offer interpretations.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.BOUNDED,
        consent_token="user-consented",
        disallowed_capabilities=["recommendation", "diagnosis"],
        phase_context={
            "phase3_complete": True,
            "stage": "post_summary"
        }
    )

    response = boundary.evaluate(request)

    # 🔒 Phase 5.3 must not conclude automatically
    assert response.status == "awaiting_resonance"

    assert response.choices is not None
    assert set(response.choices) == {
        "resonates",
        "partially_resonates",
        "does_not_resonate"
    }


# ------------------------------------------------------------
# LANGUAGE CONSTRAINTS
# ------------------------------------------------------------

def test_no_authoritative_recommendations_are_allowed():
    """
    Phase 5.3 must not provide authoritative or prescriptive guidance.
    Exploratory options are allowed, but directives are not.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    request = LLMRequest(
        user_text="Please analyze my answers and tell me what I should do next.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.BOUNDED,
        consent_token="user-consented",
        disallowed_capabilities=["recommendation", "diagnosis"],
        phase_context={
            "phase3_complete": True,
            "stage": "post_summary"
        }
    )

    response = boundary.evaluate(request)

    # ✅ Phase 5.3 proceeds, but without authority
    assert response.status == "awaiting_resonance"
    assert isinstance(response.content, list)
    assert len(response.content) >= 2

    for item in response.content:
        lowered = item.lower()
        assert "you should" not in lowered
        assert "you must" not in lowered
        assert "you need to" not in lowered
        assert "the best option" not in lowered

def test_no_fixed_identity_labels_are_used():
    """
    The system must not assign fixed or exclusive identity labels.
    Contextual pattern descriptions are allowed.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    request = LLMRequest(
        user_text="Please analyze my answers.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.BOUNDED,
        consent_token="user-consented",
        disallowed_capabilities=["recommendation", "diagnosis"],
        phase_context={
            "phase3_complete": True,
            "stage": "post_summary"
        }
    )

    response = boundary.evaluate(request)

    for item in response.content:
        lowered = item.lower()

        # ❌ Prohibited: fixed identity claims
        assert "you are a" not in lowered
        assert "this proves you are" not in lowered
        assert "this means you are" not in lowered

        # ✅ Allowed: contextual framing
        assert any(
            phrase in lowered
            for phrase in [
                "one possible interpretation",
                "may reflect",
                "could align with",
                "this approach",
                "in this context",
            ]
        )


def test_no_clinical_or_diagnostic_language():
    """
    Phase 5.3 must not resemble therapy or diagnosis.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    request = LLMRequest(
        user_text="Please analyze my answers.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.BOUNDED,
        consent_token="user-consented",
        disallowed_capabilities=["recommendation", "diagnosis"],
        phase_context={
            "phase3_complete": True,
            "stage": "post_summary"
        }
    )

    response = boundary.evaluate(request)

    for item in response.content:
        lowered = item.lower()
        assert "diagnosis" not in lowered
        assert "disorder" not in lowered
        assert "adhd" not in lowered
        assert "anxiety" not in lowered


# ------------------------------------------------------------
# FAILURE & EXIT PATHS
# ------------------------------------------------------------

def test_user_can_exit_phase5_3_without_penalty():
    """
    The user can decline interpretation and continue safely.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    request = LLMRequest(
        user_text="No thanks.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.NONE,
        consent_token=None,
        disallowed_capabilities=["recommendation", "diagnosis"],
    )

    response = boundary.evaluate(request)

    assert response.status in ("no_intelligence", "ignored", "noop")


def test_phase5_3_state_is_not_persisted_by_default():
    """
    Interpretations must not be stored unless explicitly requested.
    """

    from phase5.boundary import LLMBoundary

    boundary = LLMBoundary()

    assert not hasattr(boundary, "stored_interpretations")
    assert not hasattr(boundary, "phase5_memory")


def test_phase5_3_does_not_modify_signal_counts():
    """
    Phase 5.3 must not feed back into detection logic.
    """

    from phase5.boundary import LLMBoundary
    from phase5.request import LLMRequest
    from phase5.roles import ParticipantRole, IntelligenceMode

    boundary = LLMBoundary()

    initial_signals = ["support_seeking", "systems_thinking"]

    request = LLMRequest(
        user_text="Please analyze my answers.",
        role=ParticipantRole.OBSERVER,
        intelligence_mode=IntelligenceMode.BOUNDED,
        consent_token="user-consented",
        disallowed_capabilities=["recommendation", "diagnosis"],
        phase_context={
            "phase3_complete": True,
            "stage": "post_summary",
            "signals_visible": initial_signals.copy()
        }
    )

    boundary.evaluate(request)

    assert request.phase_context["signals_visible"] == initial_signals
