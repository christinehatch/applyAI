from .policy import validate_llm_request
from .response import LLMResponse
from .null_adapter import NullLLMAdapter
from .paraphrase_adapter import ParaphraseAdapter
from .roles import IntelligenceMode
from .bounded_adapter import BoundedInterpretationAdapter


class LLMBoundary:
    """
    Central enforcement point for Phase 5.

    Decides whether LLM participation is allowed,
    and if so, which adapter is permitted.
    """

    def __init__(self):
        self.null_adapter = NullLLMAdapter()
        self.paraphrase_adapter = ParaphraseAdapter()
        self.bounded_adapter = BoundedInterpretationAdapter()

    def evaluate(self, request):
        # --- Policy enforcement ---
        allowed, reason = validate_llm_request(request)
        if not allowed:
            return LLMResponse(status="denied", message=reason)

        # --- Phase 5.3 explicit request detection ---
        if request.intelligence_mode == IntelligenceMode.BOUNDED:
            if not self.is_explicit_interpretation_request(request.user_text):
                # Silent refusal — do NOT explain, do NOT escalate
                return self.null_adapter.evaluate(request)

            return self.bounded_adapter.evaluate(request)

        # --- Phase 5.2 ---
        if request.intelligence_mode == IntelligenceMode.SHALLOW:
            return self.paraphrase_adapter.evaluate(request)

        # --- Default ---
        return self.null_adapter.evaluate(request)

    @staticmethod
    def is_explicit_interpretation_request(text: str) -> bool:
        """
        Returns True only if the user explicitly asks
        for interpretation / analysis of prior content.
        """
        triggers = [
            "interpret",
            "analyze",
            "analysis",
            "what does this say about",
            "what does this suggest",
            "possible interpretations",
            "help me understand what this means",
        ]

        lowered = text.lower()
        return any(trigger in lowered for trigger in triggers)
