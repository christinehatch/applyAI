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
from signals import (
    SUPPORT_SIGNAL,
    detect_support_signal,
    detect_systems_signal,
    detect_exploration_signal
)
from reflections import (
    collect_reflections,
    generate_base_summary
)
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



def insight_log(event, data=None):
    print("\n🧠 INSIGHT:", event)
    if data:
        for k, v in data.items():
                print(f"  - {k}: {v}")





def generate_summary(responses, conversation_state):
    summary = []

    # 1. Base heuristic summary (from reflections module)
    summary.extend(generate_base_summary(responses))

    # 2. Phase 3 reflective snippets
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
                if detect_systems_signal(user_input):
                    conversation_state["signal_counts"]["systems_thinking"] += 1
                # Passive detection: exploration-first (summary-only)
                if detect_exploration_signal(user_input):
                    conversation_state["signal_counts"]["exploration_first"] += 1

                fired, debug_info = detect_support_signal(user_input)

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