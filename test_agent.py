# test_agent.py
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

    approved_proposal_id = None
    declined_proposal_id = None

    # ---- Phase 1: force summary + get pending proposals ----
    with app.app_context():
        from app import generate_summary, conversation_state
        from memory.storage import load_proposals

        generate_summary(
            conversation_state["responses"],
            conversation_state
        )

        owner_id = conversation_state.get("owner_id")
        proposals = load_proposals(owner_id)
        pending = [p for p in proposals if p.get("decision") == "pending"]


    # ---- Phase 2: approve first proposal, decline second ----
    if pending:
        approved_proposal_id = pending[0]["proposal_id"]
        client.post(
            f"/memory/proposals/{approved_proposal_id}/approve",
            follow_redirects=True,
        )

    if len(pending) > 1:
        declined_proposal_id = pending[1]["proposal_id"]
        client.post(
            f"/memory/proposals/{declined_proposal_id}/decline",
            follow_redirects=True,
        )

    # ---- Phase 3: read resulting memory + proposals ----
    with app.app_context():
        from memory.storage import load_memory, load_proposals

        memory_raw = load_memory(owner_id)
        # --- Assert timestamp invariant ---
        assert len(memory_raw) == 1, "Expected exactly one memory item after approval"

        item = memory_raw[0]
        assert item["created_at"] == item["updated_at"], (
            "Invariant violated: created_at and updated_at must match on creation")

        proposals_raw = load_proposals(owner_id)

        assert len(memory_raw) == 1 + 0, (
            "Declined proposals must not create memory"
        )

        # --- Assert declined proposal invariants ---
        if declined_proposal_id:
            declined = next(
                (p for p in proposals_raw if p["proposal_id"] == declined_proposal_id),
                None
            )

            assert declined is not None, "Declined proposal not found in storage"

            assert declined["decision"] == "declined"
            assert declined.get("approved_at") is None, (
                "Declined proposal must not have approved_at timestamp"
            )

    # ---- Phase 4: fetch rendered pages ----
    summary_page = client.get("/")
    memory_page = client.get("/memory")
    proposals_page = client.get("/memory/proposals")

    # ---- Assemble result LAST ----
    result = {
        "transcript": transcript,
        "approved_proposal_id": approved_proposal_id,
        "summary_html": summary_page.data.decode("utf-8"),
        "memory_html": memory_page.data.decode("utf-8"),
        "proposals_html": proposals_page.data.decode("utf-8"),
        "proposals_raw": proposals_raw,
        "memory_raw": memory_raw,
        "declined_proposal_id": declined_proposal_id,
    }

    with open("test_run_output.json", "w") as f:
        json.dump(result, f, indent=2)

    print("✅ Test run complete. Output written to test_run_output.json")

if __name__ == "__main__":
    run_test()
