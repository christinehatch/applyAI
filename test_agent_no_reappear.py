# test_agent_no_reappear.py
import json
from app import app
from test_answers import TEST_RESPONSES

def run_test():
    client = app.test_client()
    transcript = []

    # ---- Start session ----
    client.get("/")

    # Drive conversation deterministically
    for stage, answer in TEST_RESPONSES.items():
        client.post(
            "/",
            data={"user_input": answer},
            follow_redirects=True,
        )

    # ---- Force summary & get proposals ----
    with app.app_context():
        from app import get_conversation_state, OWNER_COOKIE_NAME
        conversation_state = get_conversation_state(client.get_cookie(OWNER_COOKIE_NAME).value)
        from memory.storage import load_proposals

        client.post("/memory/opt-in")  # explicit Phase 5.4 opt-in

        owner_id = conversation_state.get("owner_id")
        proposals = load_proposals(owner_id)

        pending = [p for p in proposals if p["decision"] == "pending"]
        assert pending, "Expected at least one pending proposal"

        approved_id = pending[0]["proposal_id"]

    # ---- Approve proposal ----
    client.post(
        f"/memory/proposals/{approved_id}/approve",
        follow_redirects=True,
    )

    # ---- Reload proposals from storage ----
    with app.app_context():
        from memory.storage import load_proposals

        proposals_after = load_proposals(owner_id)

        approved = next(
            p for p in proposals_after
            if p["proposal_id"] == approved_id
        )

        # 🔒 Storage invariant
        assert approved["decision"] == "approved"

        pending_after = [
            p for p in proposals_after
            if p["decision"] == "pending"
        ]

        # 🔒 Core invariant
        assert approved_id not in {
            p["proposal_id"] for p in pending_after
        }, "Approved proposal reappeared as pending"

    # ---- UI-level check ----
    proposals_page = client.get("/memory/proposals")
    html = proposals_page.data.decode("utf-8")

    approved_text = pending[0]["proposed_text"]
    approved_id = pending[0]["proposal_id"]

    assert approved_text not in html, (
        "Approved proposal text must not render in proposals page"
    )
    print("✅ Step 8.4 passed — approved proposals never reappear as pending.")

if __name__ == "__main__":
    run_test()

