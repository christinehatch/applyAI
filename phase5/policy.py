def validate_llm_request(request):
    """
    Enforces Phase 4 / Phase 5 policy constraints.
    Returns (allowed: bool, reason: Optional[str]).
    """

    # Consent is required for any intelligence beyond NONE
    if request.intelligence_mode.name != "NONE":
        if not request.consent_token:
            return False, "Missing explicit user consent"

    # Explicitly forbid recommendation capability
    if request.intelligence_mode.name != "NONE":
        if "recommendation" not in request.disallowed_capabilities:
            return False, "Recommendations must be explicitly disallowed"

    return True, None
