
# Phase 2: Adaptive Reflection (Rule-Based)
# - Detect recurring cognitive signals
# - Escalate follow-up phrasing on repetition
# - Resume core flow cleanly after reflection


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
signals = {
    "framing": [],
    "entry_point": [],
    "energy": [],
    "support": []
}
SUPPORT_SIGNAL = {
    "id": "support_seeking",
    "keywords": [
        "help", "guidance", "mentor", "feedback",
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
FOLLOW_UPS = {
    "systems": "Can you walk through how you'd structure that?",
    "exploration": "What would you want to understand before deciding?",
    "support": "What kind of guidance helps you most?"
}
MAX_STAGE = max(QUESTIONS.keys()) + 1


def debug_log(title, data=None):
    print("\n" + "-" * 40)
    print(title)
    if data is not None:
        print(data)

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
    if conversation_state["signal_escalated"].get("support_seeking"):
        summary.append(
            "Some moments in the conversation invited extra reflection, "
            "which helped clarify how you like to approach uncertainty."
        )

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

            debug_log("CONVERSATION STATE SNAPSHOT", conversation_state)

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
    return render_template("summary.html", summary = summary)


@app.route("/feedback", methods=["POST"])
def feedback():
    global conversation_state

    feedback_value = request.form.get("feedback")
    feedback_detail = request.form.get("feedback_detail")
    conversation_state["feedback"] = {
        "rating": feedback_value,
        "detail": feedback_detail
    }
    return render_template("feedback_thanks.html")

@app.route("/reset")
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