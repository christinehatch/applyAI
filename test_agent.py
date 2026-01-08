# test_agent.py
import json
from app import app
from test_answers import TEST_RESPONSES

def run_test():
    client = app.test_client()
    transcript = []

    # GET initial page
    client.get("/")

    for stage, answer in TEST_RESPONSES.items():
        response = client.post(
            "/",
            data={"user_input": answer},
            follow_redirects=True,
        )
        transcript.append({
            "stage": stage,
            "answer": answer,
            "status": response.status_code,
        })

    # 🔑 FORCE summary + proposal emission
    with app.app_context():
        from app import generate_summary, conversation_state
        _ = generate_summary(
            conversation_state["responses"],
            conversation_state
        )

    # Fetch pages after proposals exist
    summary_page = client.get("/")
    memory_page = client.get("/memory")
    proposals_page = client.get("/memory/proposals")

    result = {
        "transcript": transcript,
        "summary_html": summary_page.data.decode("utf-8"),
        "memory_html": memory_page.data.decode("utf-8"),
        "proposals_html": proposals_page.data.decode("utf-8"),
    }

    # 🔒 Safely read owner + proposals inside app context
    with app.app_context():
        from app import conversation_state
        from memory.storage import load_proposals

        owner_id = conversation_state.get("owner_id")
        print("TEST AGENT OWNER_ID:", owner_id)

        result["proposals_raw"] = load_proposals(owner_id)

    with open("test_run_output.json", "w") as f:
        json.dump(result, f, indent=2)

    print("✅ Test run complete. Output written to test_run_output.json")

if __name__ == "__main__":
    run_test()
