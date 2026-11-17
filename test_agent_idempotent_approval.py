# test_agent_idempotent_approval.py
import json
from app import app
from test_answers import TEST_RESPONSES

def run_test():
    client = app.test_client()

    # Initialize session / owner
    client.get("/")

    # Drive conversation
    for _, answer in TEST_RESPONSES.items():
        client.post("/", data={"user_input": answer}, follow_redirects=True)

    # Force summary + get proposals
    with app.app_context():
        from app import generate_summary, conversation_state
        from memory.storage import load_proposals, load_memory

        generate_summary(
            conversation_state["responses"],
            conversation_state
        )

        owner_id = conversation_state["owner_id"]
        proposals = load_proposals(owner_id)
        pending = [p for p in proposals if p["decision"] == "pending"]

        assert pending, "Expected at least one proposal to approve"

        proposal_id = pending[0]["proposal_id"]
        proposal_text = pending[0]["proposed_text"]

    # ---- First approval ----
    client.post(
        f"/memory/proposals/{proposal_id}/approve",
        follow_redirects=True,
    )

    # Capture memory after first approval
    with app.app_context():
        memory_after_first = load_memory(owner_id)
        assert len(memory_after_first) == 1
        created_at = memory_after_first[0]["created_at"]
        updated_at = memory_after_first[0]["updated_at"]

    # ---- Second approval (replay) ----
    client.post(
        f"/memory/proposals/{proposal_id}/approve",
        follow_redirects=True,
    )

    # ---- Assert idempotency ----
    with app.app_context():
        memory_after_second = load_memory(owner_id)

        assert len(memory_after_second) == 1, (
            "Approving same proposal twice must not create duplicate memory"
        )

        item = memory_after_second[0]

        assert item["text"] == proposal_text
        assert item["created_at"] == created_at
        assert item["updated_at"] == updated_at

    print("✅ Step 8.5 passed — approval is idempotent")

if __name__ == "__main__":
    run_test()

