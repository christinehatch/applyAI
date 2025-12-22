# signals.py
# ============================================================
# Signal Definitions & Detection
# ------------------------------------------------------------
# Purpose:
# Define lightweight, rule-based cognitive signals and
# how they are detected from raw user input.
#
# This module contains:
#   - signal metadata (keywords, ids)
#   - pure detection functions
#
# This module NEVER:
#   - mutates state
#   - schedules follow-ups
#   - renders UI
# ============================================================

# ----------------------------
# Support-Seeking / Uncertainty
# ----------------------------

SUPPORT_SIGNAL = {
    "id": "support_seeking",
    "keywords": [
        "help", "guidance", "mentor",
        "example", "template", "walk me through",
        "not sure", "don't know", "unsure"
    ],
    "questions": [
        "When you feel unsure, what kind of support helps most—"
        "examples, a checklist, or someone asking guiding questions?",

        # Escalation (second detection)
        "I’m noticing uncertainty coming up again — what part of this feels least clear right now?",

        # count >= 3 (plateau)
        "When this uncertainty shows up, what usually helps it ease or move forward?"

    ],
    "max_escalation": 3


}
def detect_support_signal(text):
    text = text.lower()

    matched = [kw for kw in SUPPORT_SIGNAL["keywords"] if kw in text]

    if matched:
        return True, {
            "matched_keywords": matched,
            "reason": "keyword_match"
        }

    return False, {
        "matched_keywords": [],
        "checked_keywords": SUPPORT_SIGNAL["keywords"],
        "reason": "no_keywords_matched"
    }


# ----------------------------
# Systems Thinking
# ----------------------------
SYSTEMS_SIGNAL = {
    "id": "systems_thinking",
    "keywords": [
        "system", "structure", "flow", "architecture",
        "components", "relationships", "pipeline",
        "scope", "framework"
    ]
}

def detect_systems_signal(text):
    text = text.lower()
    return any(kw in text for kw in SYSTEMS_SIGNAL["keywords"])


# ----------------------------
# Exploration-First
# ----------------------------
EXPLORATION_SIGNAL = {
    "id": "exploration_first",
    "keywords": [
        "explore", "understand", "learn", "research",
        "figure out", "clarify", "get context",
        "dig into", "experiment", "look into"
    ]
}


def detect_exploration_signal(text):
    text = text.lower()
    return any(kw in text for kw in EXPLORATION_SIGNAL["keywords"])
