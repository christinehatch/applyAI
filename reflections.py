"""
This module expects conversation_state to contain:
- signal_counts: dict
- signal_escalated: dict
"""


REFLECTION_SNIPPETS = {
    "uncertainty_observed": {
        "condition": "support_seeking_observed",
        "text": (
            "At a few points in the conversation, moments of uncertainty led you "
            "to pause and look for clarification."
        )
    },

    "uncertainty_handling": {
        "condition": "support_seeking_escalated",
        "text": (
            "When things felt unclear, you tended to look for concrete anchors — "
            "like examples, clearer expectations, or a defined scope — to decide how to move forward."
        )
    },

    "structure_orientation": {
        "condition": "systems_thinking_observed",
        "text": (
            "You often approached the problem by breaking it into parts and thinking about "
            "how those pieces fit together before taking action."
        )
    },
    "exploration_orientation": {
        "condition": "exploration_first_observed",
        "text": (
            "You often took time to explore context and possibilities "
            "before deciding how to move forward."
        )
    }
}
DEBUG_REFLECTIONS = True

def check_reflection_condition(condition, conversation_state):
    if condition == "support_seeking_escalated":
        return conversation_state["signal_escalated"].get("support_seeking", False)

    if condition == "support_seeking_observed":
        return (
            conversation_state["signal_counts"].get("support_seeking", 0) >= 2
            and not conversation_state["signal_escalated"].get("support_seeking", False)
        )

    if condition == "systems_thinking_observed":
        return conversation_state["signal_counts"].get("systems_thinking", 0) >= 1

    if condition == "exploration_first_observed":
        return conversation_state["signal_counts"].get("exploration_first", 0) >= 2

    return False

def reflection_debug(event, data=None):
    """
    Debug-only hook for Phase 3 synthesis.
    Never shown to users.
    """
    print("\n🔎 REFLECTION DEBUG:", event)
    if data:
        for k, v in data.items():
            print(f"  - {k}: {v}")


def collect_reflections(conversation_state):
    """
    Collects user-facing reflection snippets based on
    unlocked conditions. No logic or interpretation lives here.
    """

    reflections = []
    unlocked = []

    for key, snippet in REFLECTION_SNIPPETS.items():
        condition = snippet.get("condition")

        if condition and check_reflection_condition(condition, conversation_state):
            reflections.append(snippet["text"])
            unlocked.append({
                "snippet": key,
                "condition": condition
            })

    # Debug-only visibility
    if DEBUG_REFLECTIONS:
        reflection_debug(
            "Reflections collected",
            {
                "unlocked_snippets": unlocked,
                "signal_counts": conversation_state["signal_counts"],
                "signal_escalated": conversation_state["signal_escalated"]
            }
        )

    return reflections


# ------------------------------------------------------------
# Base Heuristic Summary (Pre-Reflection)
# ------------------------------------------------------------
# Purpose:
# Generate neutral, heuristic-based summary sentences
# from raw responses BEFORE reflective snippets are added.
#
# This logic:
# - Does NOT use signal counts
# - Does NOT know about escalation
# - Uses only response text
# ------------------------------------------------------------

SYSTEMS_WORDS = [
    "feature", "system", "flow", "architecture", "component",
    "integration", "interaction", "pipeline", "structure"
]

SUPPORT_WORDS = [
    "mentor", "guidance", "feedback", "example",
    "direction", "help", "support", "walk through"
]

EXPLORATION_WORDS = [
    "explore", "understand", "clarify", "figure out",
    "learn", "experiment", "research"
]


def generate_base_summary(responses):
    """
    Generates heuristic, non-reflective summary sentences
    based purely on language patterns in responses.
    """

    summary = []
    matched_any_pattern = False

    r1 = responses.get(1, "").lower()
    r2 = responses.get(2, "").lower()
    r3 = responses.get(3, "").lower()

    if any(word in r1 for word in EXPLORATION_WORDS):
        summary.append(
            "You approach new problems by exploring and understanding context before committing to solutions."
        )
        matched_any_pattern = True

    if any(word in r2 for word in SYSTEMS_WORDS):
        summary.append(
            "You tend to think in terms of systems, features, and interactions rather than linear task lists."
        )
        matched_any_pattern = True

    if any(word in r3 for word in SUPPORT_WORDS):
        summary.append(
            "You appear to benefit from external guidance or feedback when moving from ideas into execution."
        )
        matched_any_pattern = True

    if not matched_any_pattern:
        summary.append(
            "Based on your responses, you engage thoughtfully with open-ended problems, even when structure is minimal."
        )

    return summary

