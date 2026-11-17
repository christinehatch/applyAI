# test_agent_decline.py
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

    declined_proposal_id = None

    # ---- Phase 1: force summary + get proposals ----
    with app.app_context():
        from app import generate_summary, conversation_state
        from memory.storage import load_proposals

        generate_summary(
            conversation_state["responses"],
            conversation_state
        )

        owner_id = conversation_state.get("owner_id")
        proposals = load_proposals(owner_id)

        pending = [p for p in proposals if p["decision"] == "pending"]
        assert pending, "Expected at least one pending proposal to decline"

        declined_proposal_id = pending[0]["proposal_id"]

    # ---- Phase 2: DECLINE proposal via real route ----
    client.post(
        f"/memory/proposals/{declined_proposal_id}/decline",
        follow_redirects=True,
    )

    # ---- Phase 3: assert invariants ----
    with app.app_context():
        from memory.storage import load_memory, load_proposals

        memory_raw = load_memory(owner_id)
        proposals_raw = load_proposals(owner_id)

        # 🔒 Core invariant
        assert memory_raw == [], (
            "Declining a proposal must not create memory"
        )

        declined = next(
            p for p in proposals_raw
            if p["proposal_id"] == declined_proposal_id
        )

        assert declined["decision"] == "declined", "Proposal must be marked declined"
        assert declined.get("approved_at") is None, (
            "Declined proposal must not have approved_at timestamp"
        )

    result = {
        "transcript": transcript,
        "declined_proposal_id": declined_proposal_id,
        "memory_raw": memory_raw,
        "proposals_raw": proposals_raw,
    }

    with open("test_run_decline_output.json", "w") as f:
        json.dump(result, f, indent=2)

    print("✅ Decline test passed. No memory created.")

if __name__ == "__main__":
    run_test()

