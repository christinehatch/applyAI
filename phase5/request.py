from dataclasses import dataclass
from typing import Optional, List

from .roles import ParticipantRole, IntelligenceMode


@dataclass
class LLMRequest:
    """
    Structured request passed to the LLM boundary.
    This is a data container only — no logic, no inference.
    """
    user_text: str
    role: ParticipantRole
    intelligence_mode: IntelligenceMode
    consent_token: Optional[str]
    disallowed_capabilities: List[str]
