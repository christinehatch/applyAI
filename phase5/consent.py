from enum import Enum

class ConsentState(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"
def get_consent_state(proposal: dict) -> ConsentState:
    decision = proposal.get("decision")

    if decision == "approved":
        return ConsentState.APPROVED
    if decision == "declined":
        return ConsentState.DECLINED

    return ConsentState.PENDING

