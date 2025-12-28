# phase5/bounded_adapter.py

from .response import LLMResponse
from .roles import IntelligenceMode

IDENTITY_LOCKING_PHRASES = [
    "you are a ",
    "you are an ",
    "this proves you are",
    "this means you are",
    "you are inherently",
    "you are fundamentally",
]

CLINICAL_DIAGNOSTIC_TERMS = [
    # Generic medical framing
    "diagnosis",
    "diagnosed",
    "disorder",
    "condition",

    # Neuro / psych diagnoses
    "adhd",
    "autism",
    "autistic",
    "schizophrenia",
    "bipolar",
    "ocd",
    "ptsd",
    "depression",
    "anxiety",

    # Learning / neurodevelopmental labels
    "dyslexia",
    "dyspraxia",
    "tourette",
    "tourette's",

    # Framing terms that imply pathology
    "neurodivergent",
    "neurotypical",
]


AUTHORITATIVE_PHRASES = [
    "you should",
    "you must",
    "you need to",
    "the right path",
    "the best option",
    "the correct next step",
    "i recommend that you",
]

def requests_authoritative_guidance(text: str) -> bool:
    if not text:
        return False

    triggers = [
        "what should i do",
        "tell me what to do",
        "what is the best",
        "what is the right",
        "what do i need to do",
    ]

    lowered = text.lower()
    return any(t in lowered for t in triggers)

def contextualize(text: str) -> str:
    return f"One possible interpretation is that {text} in this context."


class BoundedInterpretationAdapter:
    """
    Phase 5.3 adapter.
    Produces bounded, optional interpretations only.
    """

    def evaluate(self, request):
        raw_interpretations = [
            "exploring options before committing",
            "uncertainty prompting a search for external input",
        ]

        interpretations = [
            contextualize(text)
            for text in raw_interpretations
        ]

        # Enforce language constraints
        for text in interpretations:
            lowered = text.lower()

            for term in CLINICAL_DIAGNOSTIC_TERMS:
                if term in lowered:
                    return LLMResponse(
                        status="denied",
                        message=f"Clinical language detected: '{term}'"
                    )

            for phrase in IDENTITY_LOCKING_PHRASES:
                if phrase in lowered:
                    return LLMResponse(
                        status="denied",
                        message=f"Identity locking phrase: '{phrase}'"
                    )

            for phrase in AUTHORITATIVE_PHRASES:
                if phrase in lowered:
                    return LLMResponse(
                        status="denied",
                        message=f"Authoritative language detected: '{phrase}'"
                    )

        return LLMResponse( 
            status="awaiting_resonance",
            content=interpretations,
            choices=[
                "resonates",
                "partially_resonates",
                "does_not_resonate"
            ]
        )
