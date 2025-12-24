from .response import LLMResponse


class NullLLMAdapter:
    """
    Default adapter.
    Guarantees no intelligence is active.
    """

    def evaluate(self, request):
        return LLMResponse(
            status="no_intelligence",
            message="LLM participation is disabled in this build."
        )
