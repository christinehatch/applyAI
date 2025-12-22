# ============================================================
# Signal Visibility Matrix (Phase 3)
# ------------------------------------------------------------
# Purpose:
# Define which cognitive signals influence:
#   - follow-up questions (Phase 2)
#   - summary reflection language (Phase 3)
#   - internal-only control logic
#
# IMPORTANT DESIGN CONSTRAINTS:
# - Signals are NEVER exposed to users as labels
# - No counts, thresholds, or metrics appear in summaries
# - Reflection language is observational, not diagnostic
# - Users may agree, disagree, or ignore reflections
#
# ------------------------------------------------------------
# Signal: support_seeking
# ------------------------------------------------------------
# Detected via:
#   - Keywords (e.g. "help", "mentor", "not sure")
#
# Used for:
#   - Adaptive follow-up questions (Phase 2)
#   - Escalated reflective follow-ups on recurrence
#
# Summary visibility:
#   - INDIRECT only
#   - Enables reflective language about how uncertainty
#     was approached (no mention of "support", counts, or frequency)
#
# Example reflection language:
#   "Moments of uncertainty appeared more than once, and
#    pausing to reflect seemed to help you regain clarity."
#
# ------------------------------------------------------------
# Signal: systems_thinking
# ------------------------------------------------------------
# Detected via:
#   - Structural / relational language
#     (e.g. "system", "flow", "components", "architecture")
#
# Used for:
#   - Internal pattern tracking (Phase 3)
#
# NOT used for:
#   - Adaptive follow-ups (initially)
#
# Summary visibility:
#   - INDIRECT only
#   - Appears as preference for structure or relationships
#
# Example reflection language:
#   "You often oriented yourself by clarifying structure
#    or relationships before moving forward."
#
# ------------------------------------------------------------
# Signal: overwhelmed / avoidance
# ------------------------------------------------------------
# Detected via:
#   - Language indicating shutdown, avoidance, or stuckness
#     (e.g. "too much", "I shut down", "I don't know where to start")
#
# Used for:
#   - Future adaptive reflection (Phase 3+)
#
# Summary visibility:
#   - OPTIONAL
#   - Only if paired with recovery or reflection
#
# Example reflection language:
#   "When things felt abstract or overwhelming, taking
#    a step back seemed to help you re-engage."
#
# ------------------------------------------------------------
# Signal: exploration_first
# ------------------------------------------------------------
# Detected via:
#   - Curiosity, clarification, learning-first language
#
# Used for:
#   - Summary synthesis only
#
# Summary visibility:
#   - INDIRECT
#   - Describes approach, not identity
#
# Example reflection language:
#   "You often explored context and possibilities
#    before committing to action."
#
# ------------------------------------------------------------
# Signals intentionally NOT summary-visible:
# ------------------------------------------------------------
# - execution_bias (early action preference)
# - hesitation markers without reflection
#
# These signals may guide future UX decisions
# but are not surfaced to users in Phase 3.
#
# ------------------------------------------------------------
# Guiding Principle:
# Signals inform reflection language —
# they never become conclusions.
# ============================================================

# ============================================================
# Reflection Tone Guard (Phase 3)
# ------------------------------------------------------------
# Purpose:
# Ensure all user-facing summaries remain reflective,
# non-authoritative, and non-diagnostic.
#
# This system NEVER tells users who they are.
# It offers mirrors, not conclusions.
#
# ------------------------------------------------------------
# Language Rules (Must Always Hold):
#
# ❌ Do NOT use:
#   - Personality labels ("you are a systems thinker")
#   - Absolute claims ("you always", "you never")
#   - Metrics or counts ("multiple times", "three times")
#   - Diagnostic or clinical terms
#   - Authority framing ("the system determined", "this means")
#
# ✅ Use:
#   - Observational phrasing ("appeared", "seemed to")
#   - Tentative language ("may", "often", "tended to")
#   - Time-scoped framing ("during the conversation")
#   - Process-focused descriptions (how, not what)
#
# ------------------------------------------------------------
# Reflection Principles:
#
# 1. Signals inform wording, not conclusions
#    - Internal signal logic is never exposed directly
#
# 2. Reflection is optional and reversible
#    - Users can agree, partially agree, or disagree
#
# 3. Recurrence is implied, never quantified
#    - Use phrases like "more than once" or
#      "at several points", never numbers
#
# 4. No advice yet
#    - Phase 3 reflects patterns
#    - Phase 4 may explore implications
#
# ------------------------------------------------------------
# Quick Self-Check Before Adding Any Summary Sentence:
#
# - Could a user reasonably say "That doesn't feel right"?
#   → If not, rewrite.
#
# - Does this sentence name a trait or identity?
#   → If yes, remove or soften.
#
# - Does this sound like an observer or an evaluator?
#   → Observer is correct.
#
# ------------------------------------------------------------
# Guiding Question:
# "Does this sentence help the user notice something,
#  without telling them what to conclude?"
# ============================================================

from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")
conversation_state = {
    "stage": 1,
    "responses": {},
    "followup": None,
    "followup_answers": None,
    "signal_counts": {
        "support_seeking": 0,
        "overwhelmed": 0,
        "systems_thinking": 0,
        "exploration_first": 0
    },
    "signal_escalated": {
        "support_seeking": False
    },
    "feedback": {
        "rating": "...",
        "detail": "..."
    }
}
QUESTIONS = {
    1: (
        "Imagine you’re asked to help design a new app for helping people "
        "navigate a city in a way that feels playful and less stressful.\n\n"
        "What do you think this project is asking for?"
    ),
    2: "How would you actually start working on this?",
    3: "What feels most challenging or uncertain when you think about executing this idea?"
}

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
SYSTEMS_SIGNAL = {
    "id": "systems_thinking",
    "keywords": [
        "system", "structure", "flow", "architecture",
        "components", "relationships", "pipeline",
        "scope", "framework"
    ]
}

EXPLORATION_SIGNAL = {
    "id": "exploration_first",
    "keywords": [
        "explore", "understand", "learn", "research",
        "figure out", "clarify", "get context",
        "dig into", "experiment", "look into"
    ]
}

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
FOLLOW_UPS = {
    "systems": "Can you walk through how you'd structure that?",
    "exploration": "What would you want to understand before deciding?",
    "support": "What kind of guidance helps you most?"
}
MAX_STAGE = max(QUESTIONS.keys()) + 1

# Internal-only interpretation of user feedback
# NEVER shown to users
FEEDBACK_INTERPRETATION = {
    "yes": "aligned",
    "somewhat": "partially_aligned",
    "no": "misaligned"
}


def debug_log(title, data=None):
    print("\n" + "-" * 40)
    print(title)
    if data is not None:
        print(data)


def reflection_debug(event, data=None):
    """
    Debug-only hook for Phase 3 synthesis.
    Never shown to users.
    """
    print("\n🔎 REFLECTION DEBUG:", event)
    if data:
        for k, v in data.items():
            print(f"  - {k}: {v}")

def insight_log(event, data=None):
    print("\n🧠 INSIGHT:", event)
    if data:
        for k, v in data.items():
                print(f"  - {k}: {v}")


def detect_support_signal_with_debug(text):
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
def detect_systems_signal_with_debug(text):
    text = text.lower()

    matched = [
        kw for kw in SYSTEMS_SIGNAL["keywords"]
        if kw in text
    ]

    if matched:
        return True, {
            "matched_keywords": matched,
            "reason": "keyword_match"
        }

    return False, {
        "matched_keywords": [],
        "checked_keywords": SYSTEMS_SIGNAL["keywords"],
        "reason": "no_keywords_matched"
    }
def detect_exploration_signal(text):
    text = text.lower()
    return any(kw in text for kw in EXPLORATION_SIGNAL["keywords"])

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
    reflection_debug(
        "Reflections collected",
        {
            "unlocked_snippets": unlocked,
            "signal_counts": conversation_state["signal_counts"],
            "signal_escalated": conversation_state["signal_escalated"]
        }
    )

    return reflections


def generate_summary(responses, conversation_state):
    summary = []
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
    matched_any_pattern = True

    response = responses.get(1, "").lower()

    if any(word in response for word in EXPLORATION_WORDS):
        summary.append(
            "You approach new problems by exploring and understanding context before committing to solutions."
        )
        matched_any_pattern = False

    response = responses.get(2, "").lower()

    if any(word in response for word in SYSTEMS_WORDS):
        summary.append(
            "You tend to think in terms of systems, features, and interactions rather than linear task lists."
        )
        matched_any_pattern = False

    response = responses.get(3, "").lower()

    if any(word in response for word in SUPPORT_WORDS):
        summary.append(
            "You appear to benefit from external guidance or feedback when moving from ideas into execution."
        )
        matched_any_pattern = False
    if matched_any_pattern:
        summary.append("Based on your responses, you tend to engage thoughtfully with open-ended problems, even when structure is minimal.")

    # Meta-reflection (no labels, no counts, no signals)
    reflections = collect_reflections(conversation_state)
    summary.extend(reflections)

    debug_log("SUMMARY FEEDBACK ALIGNMENT", {
        "interpretation": conversation_state["feedback"].get("interpretation"),
        "signals_visible": [
            k for k, v in conversation_state["signal_counts"].items()
            if v > 0
        ]
    })

    return " ".join(summary)



@app.route("/", methods=["GET", "POST"])
def home():
    global conversation_state
    stage = conversation_state["stage"]

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()

        if user_input:

            debug_log("USER INPUT", {
                "stage": conversation_state["stage"],
                "text": user_input,
                "followup_active": bool(conversation_state["followup"])
            })

            # CASE 1: answering a follow-up
            if conversation_state["followup"]:
                conversation_state["followup_answers"] = user_input
                conversation_state["followup"] = None
                conversation_state["stage"] += 1

                debug_log("FOLLOW-UP ANSWER STORED", {
                    "answer": user_input,
                    "next_stage": conversation_state["stage"]
                })

            # CASE 2: normal stage response
            else:
                stage = conversation_state["stage"]
                conversation_state["responses"][stage] = user_input

                # Passive detection: systems thinking (summary-only)
                if detect_systems_signal_with_debug(user_input):
                    conversation_state["signal_counts"]["systems_thinking"] += 1
                # Passive detection: exploration-first (summary-only)
                if detect_exploration_signal(user_input):
                    conversation_state["signal_counts"]["exploration_first"] += 1

                fired, debug_info = detect_support_signal_with_debug(user_input)

                if fired:
                    conversation_state["signal_counts"]["support_seeking"] += 1
                    count =  conversation_state["signal_counts"]["support_seeking"]

                    if count <= len(SUPPORT_SIGNAL["questions"]):
                        conversation_state["followup"] = SUPPORT_SIGNAL["questions"][count - 1]

                        # Lock escalation after the last reflective question
                        if count == SUPPORT_SIGNAL["max_escalation"]:
                            conversation_state["signal_escalated"]["support_seeking"] = True
                    else:
                        # After this point, the system still notices the pattern,
                        # but chooses not to interrupt the main flow again.
                        debug_log("SUPPORT SIGNAL OBSERVED (NO ESCALATION)", {
                            "count": count,
                            "reason": "already_escalated"
                        })

                    # If the signal fired but we intentionally did not interrupt,
                    # continue normal stage progression
                    if conversation_state["followup"] is None:
                        conversation_state["stage"] += 1

                    debug_log("SUPPORT SIGNAL FIRED", {
                        "signal": SUPPORT_SIGNAL["id"],
                        "details": debug_info
                    })

                else:
                    conversation_state["stage"] += 1

                    debug_log("SUPPORT SIGNAL NOT FIRED", {
                        "signal": SUPPORT_SIGNAL["id"],
                        "details": debug_info
                    })
            debug_log("STATE SUMMARY", {
                "stage": conversation_state["stage"],
                "followup_active": bool(conversation_state["followup"]),
                "support_count": conversation_state["signal_counts"]["support_seeking"],
                "support_escalated": conversation_state["signal_escalated"]["support_seeking"]
            })

            stage = conversation_state["stage"]

    if stage in QUESTIONS:
        question = QUESTIONS[stage]
        return render_template(
            "index.html",
            stage=stage,
            question=QUESTIONS.get(stage),
            followup=conversation_state["followup"]
        )

    # Otherwise, show summary
    summary = generate_summary(
        conversation_state["responses"],
        conversation_state
    )
    debug_log("SESSION INTERPRETATION", {
        "signal_counts": conversation_state["signal_counts"],
        "escalations": conversation_state["signal_escalated"],
        "user_feedback": conversation_state["feedback"]
    })
    return render_template("summary.html", summary = summary)


@app.route("/feedback", methods=["POST"])
def feedback():
    global conversation_state

    feedback_value = request.form.get("feedback")
    feedback_detail = request.form.get("feedback_detail")

    interpretation = FEEDBACK_INTERPRETATION.get(
        feedback_value,
        "unknown"
    )

    conversation_state["feedback"] = {
        "rating": feedback_value,
        "detail": feedback_detail,
        "interpretation": interpretation
    }

    debug_log("USER FEEDBACK RECEIVED", {
        "rating": feedback_value,
        "interpretation": interpretation,
        "detail": feedback_detail,
        "signal_counts": conversation_state["signal_counts"],
        "signal_escalated": conversation_state["signal_escalated"]
    })

    return render_template("feedback_thanks.html")


def reset():
    global conversation_state
    conversation_state = {
        "stage": 1,
        "responses": {},
        "followup": None,
        "followup_answers": None,
        "signal_counts": {
            "support_seeking": 0,
            "overwhelmed": 0,
            "systems_thinking": 0,
            "exploration_first": 0
        },
        "signal_escalated": {
            "support_seeking": False
        },
        "feedback": {
            "rating": "...",
            "detail": "..."
        }
    }
    return "Conversation reset"

if __name__ == "__main__":
    app.run(debug=True)