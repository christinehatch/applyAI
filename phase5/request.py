from dataclasses import dataclass
from typing import Optional, List, Dict, Any

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
    content_type: Optional[str] = None # "question" | "summary" | None
    phase_context: Optional[Dict[str, Any]] = None  # ✅ FIXED

