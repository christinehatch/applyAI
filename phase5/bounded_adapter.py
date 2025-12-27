# phase5/bounded_adapter.py

from .response import LLMResponse
from .roles import IntelligenceMode

FORBIDDEN_PHRASES = [
    "you are",
    "this means you should",
    "i recommend",
    "you should",
    "diagnosis",
    "disorder",
    "adhd",
    "anxiety",
]

class BoundedInterpretationAdapter:
    """
    Phase 5.3 adapter.
    Produces bounded, optional interpretations only.
    """

    def evaluate(self, request):
        # Placeholder content until generation is implemented
        interpretations = [
            "One possible way to read this is that you were exploring options before committing.",
            "Another interpretation could be that uncertainty prompted you to seek external input."
        ]

        # Enforce language constraints
        for text in interpretations:
            lowered = text.lower()
            for phrase in FORBIDDEN_PHRASES:
                if phrase in lowered:
                    return LLMResponse(
                        status="denied",
                        message=f"Forbidden phrase detected: '{phrase}'"
                    )

        return LLMResponse(
            status="ok",
            content=interpretations,
            mode=IntelligenceMode.BOUNDED
        )