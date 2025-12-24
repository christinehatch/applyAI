from .policy import validate_llm_request
from .response import LLMResponse
from .null_adapter import NullLLMAdapter
from .paraphrase_adapter import ParaphraseAdapter
from .roles import IntelligenceMode


class LLMBoundary:
    """
    Central enforcement point for Phase 5.

    Decides whether LLM participation is allowed,
    and if so, which adapter is permitted.
    """

    def __init__(self, adapter=None):
        # Default to null behavior unless explicitly allowed
        self.null_adapter = NullLLMAdapter()
        self.paraphrase_adapter = ParaphraseAdapter()

    def evaluate(self, request):
        # Phase 5 policy enforcement
        allowed, reason = validate_llm_request(request)
        if not allowed:
            return LLMResponse(status="denied", message=reason)

        # Route based on intelligence mode
        if request.intelligence_mode == IntelligenceMode.SHALLOW:
            return self.paraphrase_adapter.evaluate(request)

        # Default: no intelligence
        return self.null_adapter.evaluate(request)
