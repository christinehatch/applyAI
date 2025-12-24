from enum import Enum


class ParticipantRole(Enum):
    """
    Defines how the LLM is allowed to participate.
    No role implies authority or decision-making.
    """
    PARTICIPANT = "participant"
    MIRROR = "mirror"
    OBSERVER = "observer"


class IntelligenceMode(Enum):
    """
    Defines the level of intelligence explicitly requested.
    Default is NONE.
    """
    NONE = "none"
    SHALLOW = "shallow"
    DELIBERATIVE = "deliberative"
