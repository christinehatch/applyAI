# Phase 5.4 — Longitudinal Awareness Checklist (Implementation-Tracked)

> Core question: **Can insight persist without identity being imposed?**

**Status meanings**
- ✅ Implemented + tested  
- 🟡 Partially implemented (core primitive exists, not integrated into product flow)  
- ⛔ Not implemented  
- ➖ Not applicable yet (no runtime consumer exists; guarded at the boundary)

**Integration tests:** `tests/test_phase5_4_integration.py` (real routes, temp storage)
**Primitive tests:** `tests/test_phase5_4_memory.py`
**Harnesses:** `test_agent*.py` (drive the full flow through `/memory/opt-in`)

---

## 0) Current Status Snapshot

- [x] ✅ Phase 5.4 **memory primitives exist** (schema, store, proposal workflow, selection builder).
- [x] ✅ Phase 5.4 **is integrated** into runtime UI/flow (opt-in, proposals, approve/decline, ledger, forget, selection).
- [x] ✅ Phase 5.4 has dev-only file-backed persistence (JSON per owner_id).
- [x] ✅ Stable anonymous owner_id exists (cookie-based; no login), and conversation state is isolated per owner.

---

## 1) Entry & Risk Gating (High-Risk Surface)

- [x] ✅ Phase 5.4 is **opt-in only**: proposals are created only by `POST /memory/opt-in`, an explicit user action on the summary page.
- [x] ✅ Consent is **separate from Phase 5.3**: memory opt-in neither reads nor sets `phase5_consent_token`; the Phase 5 consent offer creates no proposals.
- [x] ✅ Phase ordering enforced: `/memory/opt-in` returns 409 until the Phase 3 summary exists (`summary_ready`).
- [x] ✅ No memory logic reachable without explicit user action: `generate_summary()` records reflections but writes nothing.
- [x] ✅ No automatic upgrades into memory mode; opt-in is per conversation and idempotent.

**Evidence:** `test_summary_alone_creates_no_proposals_and_offers_opt_in`, `test_opt_in_before_summary_is_rejected`, `test_opt_in_after_summary_creates_pending_proposals_only_once`, `test_memory_opt_in_is_separate_from_phase5_consent`, `test_phase5_consent_offer_does_not_create_proposals`

---

## 2) Memory Object Model (Minimum Schema)

- [x] ✅ `MemoryItem` exists with required fields (id, owner_id, text, kind, source, timestamps, status).
- [x] ✅ `MemoryProposal` exists with proposal workflow fields and decision states.
- [x] ✅ `MemorySource` exists (provenance).
- [x] ✅ `SelectedMemoryContext` exists (ephemeral retrieval container).
- [x] ✅ `MemoryKind` allowlist exists: **PREFERENCE / CONSTRAINT / GOAL / SELF_OBSERVATION**, and the approve route rejects anything else.

**Evidence:** `phase5/memory.py`; `test_approve_rejects_kind_outside_allowlist`

---

## 3) Proposal-Before-Write (Core Ethical Mechanism)

- [x] ✅ Proposal does **not** create stored memory.
- [x] ✅ Approval creates a `MemoryItem` from the proposal text only, through `FileBackedMemoryStore.create()`.
- [x] ✅ Approval timestamps are server-generated ISO-8601 with `created_at == updated_at`.
- [x] ✅ Decline creates **no** memory item and does not retain the proposal text.
- [x] ✅ Declined proposals cannot later be approved (state transition blocked; replays are no-ops).

**Evidence:** `tests/test_phase5_4_memory.py`, `test_approve_writes_iso_timestamps_and_source_through_store`, `test_decline_does_not_retain_proposal_text`, `test_agent_idempotent_approval.py`

---

## 4) Mechanical Content Constraints (Identity / Clinical / Authority Blocks)

- [x] ✅ Memory text validator exists and runs on approval (storage-time).
- [x] ✅ Blocks identity-locking language.
- [x] ✅ Blocks clinical/diagnostic terms.
- [x] ✅ Blocks authoritative/prescriptive phrasing.
- [x] ✅ A blocked approval returns 400 and leaves the proposal pending (no partial write).

**Evidence:** `test_validator_blocks_identity_clinical_and_authoritative_language`, `test_approve_rejects_identity_locking_text_and_keeps_proposal_pending`

---

## 5) Forgetting Guarantees (Non-Use)

- [x] ✅ Delete sets item status to `"deleted"` and timestamps (idempotent).
- [x] ✅ Deleted items do not appear in ledger list (`store.list()` returns active only).
- [x] ✅ Deleted items persist as deleted and are not reloaded as active.
- [x] ✅ User-facing "Forget this" button and `POST /memory/<id>/forget` route (soft delete; 404 for unknown or other owners' ids).
- [x] ✅ Forgetting also removes the item from the current selection.

**Evidence:** `test_forget_removes_item_from_ledger_and_soft_deletes`, `test_forget_is_idempotent_and_unknown_id_is_404`, `test_selection_is_cleared_by_clear_forget_and_reset_and_never_persisted`

---

## 6) Retrieval & Use Constraints (No Auto-Consumption)

- [x] ✅ Selection context builder requires explicit selected IDs (no implicit recall).
- [x] ✅ If selection is empty, context is empty and has no attribution line.
- [x] ✅ Attribution line appears only when memory is actually used.
- [x] ✅ A UI that lets the user select memory items (`/memory/select`). Selection is session-only, never written to disk, and cleared by "Stop using these items" and `/reset`.
- [x] ✅ Single boundary for downstream use: `build_selected_memory_context()` is the only function that resolves memory for use, and it resolves only selected, active, same-owner items.
- [ ] ➖ Prompt injection into Phase 5.3: Phase 5.3 interpretation is not wired into the runtime yet, so there is no prompt to inject into. Any future consumer (Phase 5.3 or Phase 6) must go through `build_selected_memory_context()` and show its attribution line.

**Evidence:** `test_no_memory_is_used_until_selected`, `test_selected_memory_is_used_with_attribution`

---

## 7) Ownership Isolation (Owner ID Boundary)

- [x] ✅ All memory objects include `owner_id` and store is keyed by owner.
- [x] ✅ Owner ID exists in the product/runtime (stable per user across sessions).
- [x] ✅ Ownership isolation enforced structurally (per-owner directories; per-owner conversation state).
- [x] ✅ Adversarial cross-owner tests: another owner cannot see, forget, approve, decline, or select someone else's items.

**Evidence:** `test_other_owner_cannot_see_forget_approve_or_select_my_memory`, `tests/test_per_owner_state.py`

---

## 8) Memory Ledger (User-Visible)

- [x] ✅ User can view all active stored memory items (`/memory`).
- [x] ✅ Ledger shows exact wording (verbatim), created_at, kind, source.
- [x] ✅ Ledger supports delete/forget.
- [x] ✅ "What I remember" is a first-class view, linked from the summary page.

---

## 9) Persistence Layer (Required for "Longitudinal")

- [x] ✅ Persistence location chosen (dev-only, file-backed, repo-local).
- [x] ✅ File-backed storage backend implemented (JSON per owner_id).
- [x] ✅ Persistence respects ownership boundaries.
- [x] ✅ Persistence respects deletion (non-use), including across restarts.
- [x] ✅ Migration strategy documented: see "Storage Versions" in `phase5_4_memory_schema.md`.

**Evidence:** `test_memory_survives_restart_and_deletion_persists`, `test_legacy_v0_records_are_read_with_their_real_timestamps`

---

## 10) No Application Leakage (Hard Boundary)

- [x] ✅ Phase 5.4 primitives contain no career planning / project suggestion logic.
- [x] ✅ Integration introduced none of the following (reviewed in the Phase 5.4 completion change):
  - [x] ✅ project suggestions
  - [x] ✅ job targeting
  - [x] ✅ resume language
  - [x] ✅ planning/optimization language

**Rule:** Memory management only in Phase 5.4.

---

## 11) Test Coverage

**Primitive-level**
- [x] ✅ Proposal-before-write
- [x] ✅ Decline-no-side-effects
- [x] ✅ Delete-means-non-use
- [x] ✅ Validator enforcement
- [x] ✅ No auto-consumption on empty selection

**Integration-level**
- [x] ✅ Opt-in gating / consent separation from Phase 5.3
- [x] ✅ Phase ordering (memory proposals only after reflection)
- [x] ✅ Persistence backend tests (create/list/delete across restarts, legacy records)
- [x] ✅ Cross-owner isolation tests
- [x] ✅ UI selection → context + attribution appears when used
- [ ] ➖ Prompt injection test: waits for the first runtime consumer (see §6)

---

## 12) Final Phase 5.4 Invariant

- [x] ✅ Encoded into design + enforced mechanically at storage-time:

> **"The system can remember what the user approved, without deciding who the user is."**
