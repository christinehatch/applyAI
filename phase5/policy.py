from .roles import IntelligenceMode


def validate_llm_request(request):
    """
    Central policy enforcement for Phase 5.
    Returns (allowed: bool, reason: Optional[str]).
    """

    # --- Phase ordering enforcement (HARD BLOCK) ---
    if request.intelligence_mode in (
        IntelligenceMode.BOUNDED,
        IntelligenceMode.DELIBERATIVE,
    ):
        phase_context = request.phase_context

        if not phase_context:
            return False, "Phase context missing"

        if not phase_context.get("phase3_complete"):
            return False, "Phase 3 reflection not complete"

        if phase_context.get("stage") != "post_summary":
            return False, "Phase 5.3 only allowed after summary"

    # --- Consent gating ---
    if request.intelligence_mode != IntelligenceMode.NONE:
        if not request.consent_token:
            return False, "Missing explicit user consent"

        if "recommendation" not in request.disallowed_capabilities:
            return False, "Recommendations must be explicitly disallowed"

    return True, None
