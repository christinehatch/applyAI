from .roles import IntelligenceMode


def is_explicit_phase5_3_request(user_text: str) -> bool:
    """
    Detects whether the user explicitly requests interpretation.
    This must be conservative — false negatives are safer than false positives.
    """
    if not user_text:
        return False

    triggers = [
        "interpret",
        "possible meanings",
        "what might this say",
        "reflect on",
        "what does this suggest",
        "patterns in my responses",
        "multiple interpretations"
    ]

    text = user_text.lower()
    return any(t in text for t in triggers)


def validate_llm_request(request):
    """
    Central policy enforcement for Phase 5.
    Returns (allowed: bool, reason: Optional[str]).
    """
    # --- Consent gating ---
    if request.intelligence_mode != IntelligenceMode.NONE:
        if not request.consent_token:
            return False, "Missing explicit user consent"

        # Recommendations must always be disallowed
        if "recommendation" not in request.disallowed_capabilities:
            return False, "Recommendations must be explicitly disallowed"

    return True, None

    if request.intelligence_mode == IntelligenceMode.BOUNDED:
        phase_context = getattr(request, "phase_context", None)

        if not phase_context:
            return False, "Phase context missing"

        if not phase_context.get("phase3_complete"):
            return False, "Phase 3 reflection not complete"

        if phase_context.get("stage") != "post_summary":
            return False, "Phase 5.3 only allowed after summary"
        if not is_explicit_phase5_3_request(request.user_text):
            return False, "Explicit interpretation request required"



