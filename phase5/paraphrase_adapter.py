# phase5/paraphrase_adapter.py

from .response import LLMResponse
from .request import LLMRequest


class ParaphraseAdapter:
    """
    Deterministic, consent-gated paraphrasing adapter.
    No interpretation, no analysis — wording only.
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

        # SAFETY CHECK: only operate on known content types
        if request.content_type != "question":
            return LLMResponse(
                status="ignored",
                message="Paraphrasing skipped for non-question content."
            )

        original = request.user_text.strip()

        # --- Deterministic paraphrase (editorial rewrite, no inference) ---
        paraphrased = (
            "Here’s the same question phrased a bit more directly:\n\n"
            "You’re designing an app meant to help people navigate a city "
            "in a way that feels playful and less stressful. "
            "What do you think the core goal of this project is?"
        )

        return LLMResponse(
            status="paraphrased",
            content=paraphrased
        )
