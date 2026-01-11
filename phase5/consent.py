from enum import Enum

class ConsentState(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"


def get_consent_state(proposal: dict) -> ConsentState:
    try:
        return ConsentState(proposal.get("decision", "pending"))
    except ValueError:
        return ConsentState.PENDING