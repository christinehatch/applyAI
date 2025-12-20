from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")
MAX_STAGE = 4
conversation_state = {
    "stage": 1,
    "responses": {},
    "feedback": {
        "rating": "...",
        "detail": "..."
    }
}


def generate_summary(responses):
    summary = []

    if responses.get(1):
        summary.append(
            "You begin by interpreting the problem broadly and exploring possibilities."
        )

    if responses.get(2) and "feature" in responses[2].lower():
        summary.append(
            "You tend to think in terms of features and systems rather than step-by-step tasks."
        )

    if responses.get(3) and "mentor" in responses[3].lower():
        summary.append(
            "You benefit from guidance or feedback when moving from ideas into execution."
        )

    return " ".join(summary)


@app.route("/", methods=["GET", "POST"])
def home():
    global conversation_state
    stage = conversation_state["stage"]

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()

        if user_input:
            conversation_state["responses"][stage] = user_input
            if (stage < MAX_STAGE):
                conversation_state["stage"] += 1
                stage = conversation_state["stage"]

    if stage == 1:
        question = (
            "Imagine you’re asked to help design a new app for helping people "
            "navigate a city in a way that feels playful and less stressful.\n\n"
            "What do you think this project is asking for?"
        )

    elif stage == 2:
        question = "How would you actually start working on this?"

    elif stage == 3:
        question = (
            "What feels most challenging or uncertain when you think about executing this idea?"
        )
    elif stage == 4:
        summary = generate_summary(conversation_state["responses"])
        return render_template(
            "summary.html",
            summary=summary
        )

    else:
        question = "Thank you for your responses."

    return render_template(
        "index.html",
        stage=stage,
        question=question
    )

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
    conversation_state["stage"] = 1
    conversation_state["responses"] = {}
    return "Conversation reset"


if __name__ == "__main__":
    app.run(debug=True)