from .policy import validate_llm_request
from .response import LLMResponse


class LLMBoundary:
    """
    Single entry point for any LLM participation.
    All policy checks happen here before delegation.
    """

    def __init__(self, adapter):
        self.adapter = adapter

    def evaluate(self, request):
        allowed, reason = validate_llm_request(request)

        if not allowed:
            return LLMResponse(
                status="denied",
                message=reason
            )

        return self.adapter.evaluate(request)
