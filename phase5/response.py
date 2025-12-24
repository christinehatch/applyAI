from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMResponse:
    """
    Structured response from the LLM boundary.
    Even null or disabled responses must conform.
    """
    status: str
    message: Optional[str] = None
    content: Optional[str] = None
