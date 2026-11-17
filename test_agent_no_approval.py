# test_agent_no_approval.py
import json
from app import app
from test_answers import TEST_RESPONSES

def run_test():
    client = app.test_client()
    transcript = []

    # GET initial page (sets cookie / owner)
    client.get("/")

    # Drive conversation deterministically
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

    # ---- Phase 1: force summary ONLY ----
    with app.app_context():
        from app import generate_summary, get_conversation_state, OWNER_COOKIE_NAME
        conversation_state = get_conversation_state(client.get_cookie(OWNER_COOKIE_NAME).value)
        from memory.storage import load_memory, load_proposals

        generate_summary(
            conversation_state["responses"],
            conversation_state
        )

        owner_id = conversation_state.get("owner_id")

        memory_raw = load_memory(owner_id)
        proposals_raw = load_proposals(owner_id)

        # 🔒 Core invariant
        assert memory_raw == [], (
            "Memory must remain empty when no proposal is approved"
        )

        # Optional sanity check
        assert all(p["decision"] == "pending" for p in proposals_raw), (
            "Proposals should remain pending without user action"
        )

    result = {
        "transcript": transcript,
        "memory_raw": memory_raw,
        "proposals_raw": proposals_raw,
    }

    with open("test_run_no_approval_output.json", "w") as f:
        json.dump(result, f, indent=2)

    print("✅ No-approval test passed. Memory remains empty.")

if __name__ == "__main__":
    run_test()

