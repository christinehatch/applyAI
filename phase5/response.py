from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class LLMResponse:
    """
    Structured response returned from the LLM boundary or adapters.
    """
    status: str
    message: Optional[str] = None
    content: Optional[Any] = None
    choices: Optional[list] = None
