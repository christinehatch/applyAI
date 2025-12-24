from .response import LLMResponse
from .request import LLMRequest


class ParaphraseAdapter:
    """
    Phase 5.2 adapter: language-only participation.

    This adapter is intentionally limited to surface-level
    language transformation. It must never:
    - introduce new meaning
    - analyze user intent
    - synthesize signals
    - infer traits or conclusions

    In Phase 5.2, this adapter may only be used to rephrase
    system-authored text (questions or summaries), never
    raw user input.
    """

    def evaluate(self, request: LLMRequest) -> LLMResponse:
        # SAFETY CHECK: adapter should only run with explicit consent
        if request.consent_token is None:
            return LLMResponse(
                status="denied",
                message="Consent required for paraphrasing."
            )

        # SAFETY CHECK: only shallow intelligence is allowed
        if request.intelligence_mode.name != "SHALLOW":
            return LLMResponse(
                status="denied",
                message="Paraphrasing only allowed in SHALLOW mode."
            )

        # SAFETY CHECK: never touch raw user input
        if request.content_type is None:
            return LLMResponse(
                status="skipped",
                message="No paraphrasable content provided."
            )

        # Phase 5.2 stub behavior:
        # For now, simply return the text unchanged.
        # This proves routing without introducing intelligence.
        return LLMResponse(
            status="paraphrased",
            content=request.user_text
        )
