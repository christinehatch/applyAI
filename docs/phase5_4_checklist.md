# Phase 5.4 — Longitudinal Awareness Checklist (Implementation-Tracked)

> Core question: **Can insight persist without identity being imposed?**

**Status meanings**
- ✅ Implemented + tested  
- 🟡 Partially implemented (core primitive exists, not integrated into product flow)  
- ⛔ Not implemented  

---

## 0) Current Status Snapshot

- [x] ✅ Phase 5.4 **memory primitives exist** (schema, store, proposal workflow, selection builder).
- [ ] ✅ Phase 5.4 **is  integrated** into runtime UI/flow yet (no routes, no templates, no gating).
- [x] ✅ Phase 5.4 has dev-only file-backed persistence (JSON per owner_id)
- [x] 🟡 Stable anonymous owner_id exists (cookie-based; no login).

**Evidence:** `phase5/memory.py`, `tests/test_phase5_4_memory.py`

---

## 1) Entry & Risk Gating (High-Risk Surface)

- [ ] ⛔ Phase 5.4 is **opt-in only** (separate explicit action from user).
- [ ] ⛔ Consent is **separate from Phase 5.3** (no shared tokens; no accidental upgrade).
- [ ] ⛔ Phase ordering enforced:
- [ ] ⛔ Memory proposals only happen after Phase 3 reflection and/or Phase 5.3 resonance loop completes.
- [ ] ⛔ No memory logic reachable without explicit user action (no implicit “helpful remembering”).
- [ ] ⛔ No automatic upgrades into memory mode.

**Notes**
- Right now: primitives exist, but nothing is wired into runtime so this gating is not yet implemented.

---

## 2) Memory Object Model (Minimum Schema)

- [x] ✅ `MemoryItem` exists with required fields (id, owner_id, text, kind, source, timestamps, status).
- [x] ✅ `MemoryProposal` exists with proposal workflow fields and decision states.
- [x] ✅ `MemorySource` exists (provenance).
- [x] ✅ `SelectedMemoryContext` exists (ephemeral retrieval container).
- [x] ✅ `MemoryKind` allowlist exists: **PREFERENCE / CONSTRAINT / GOAL / SELF_OBSERVATION**.

**Evidence:** `phase5/memory.py`

---

## 3) Proposal-Before-Write (Core Ethical Mechanism)

- [x] ✅ Proposal does **not** create stored memory.
- [x] ✅ Approval creates a `MemoryItem` from **final_text** only.
- [x] ✅ Decline creates **no** memory item.
- [x] ✅ Declined proposals cannot later be approved (state transition blocked).

**Evidence:** `tests/test_phase5_4_memory.py::test_proposal_before_write...`, `...decline_has_no_side_effects...`

---

## 4) Mechanical Content Constraints (Identity / Clinical / Authority Blocks)

- [x] ✅ Memory text validator exists and runs on approval (storage-time).
- [x] ✅ Blocks identity-locking language.
- [x] ✅ Blocks clinical/diagnostic terms.
- [x] ✅ Blocks authoritative/prescriptive phrasing.

**Evidence:** `validate_memory_text()` + `approve()` calls it; test: `test_validator_blocks_identity_clinical_and_authoritative_language`

---

## 5) Forgetting Guarantees (Non-Use)

- [x] ✅ Delete sets item status to `"deleted"` and timestamps (idempotent).
- [x] ✅ Deleted items do not appear in ledger list (`store.list()` returns active only).
- [x] ✅ Deleted items persist as deleted and are not reloaded as active

**Evidence:** `store.delete()` + `store.list()` + selection builder behavior; test: `test_delete_means_non_use...`

**Missing product behaviors**
- [ ] ⛔ User-facing “Forget” UI and routes.
- [ ] ⛔ Persistence-layer delete (once persistence exists).

---

## 6) Retrieval & Use Constraints (No Auto-Consumption)

- [x] ✅ Selection context builder requires explicit selected IDs (no implicit recall).
- [x] ✅ If selection is empty, context is empty and has no attribution line.
- [x] ✅ Attribution line appears only when memory is actually used.

**Evidence:** `MemorySelectionContextBuilder.build()`; test: `test_empty_selection_does_not_auto_consume_memory...`

**Missing product behaviors**
- [ ] ⛔ A UI that lets the user select memory items.
- [ ] ⛔ A boundary in Phase 5.3 / prompt-building that injects only selected memory + attribution.

---

## 7) Ownership Isolation (Owner ID Boundary)

- [x] ✅ All memory objects include `owner_id` and store is keyed by owner.
- [x] ✅ Owner ID exists in the product/runtime (stable per user across sessions).
- [ ] 🟡 Ownership isolation enforced structurally (per-owner directories)
- [ ] ⛔ No adversarial cross-owner tests yet
**Evidence (partial):** types include `owner_id`, store is per-owner.  
**Missing:** real `owner_id` source + persistence-level enforcement.

---

## 8) Memory Ledger (User-Visible)

- [ ] ⛔ User can view all stored memory items.
- [ ] ⛔ Ledger shows exact wording (verbatim), created_at, kind, source.
- [ ] ⛔ Ledger supports delete/forget.
- [ ] ⛔ Ledger supports “show me what you remember” as a first-class view.

**Note:** The store can list items already; the UI layer is missing.

---

## 9) Persistence Layer (Required for “Longitudinal”)

- [x] ✅ Persistence location chosen (dev-only, file-backed, repo-local)
- [x] ✅ File-backed storage backend implemented (JSON per owner_id)
- [x] ✅ Persistence respects ownership boundaries
- [x] ✅ Persistence respects deletion (non-use)
- [ ] ⛔ Migration strategy documented (even if trivial v0->v1).

---

## 10) No Application Leakage (Hard Boundary)

- [x] ✅ Phase 5.4 primitives contain no career planning / project suggestion logic.
- [ ] ⛔ Integration must not introduce:
  - [ ] ⛔ project suggestions
  - [ ] ⛔ job targeting
  - [ ] ⛔ resume language
  - [ ] ⛔ planning/optimization language

**Rule:** Memory management only in Phase 5.4.

---

## 11) Test Coverage (What exists vs what’s missing)

**Implemented tests**
- [x] ✅ File-backed persistence sanity test (manual terminal verification)
- [x] ✅ Proposal-before-write
- [x] ✅ Decline-no-side-effects
- [x] ✅ Delete-means-non-use
- [x] ✅ Validator enforcement
- [x] ✅ No auto-consumption on empty selection

**Missing tests (integration-level)**
- [ ] ⛔ Opt-in gating / consent separation from Phase 5.3
- [ ] ⛔ Phase ordering (memory proposals only after reflection/interpretation loop)
- [ ] ⛔ Persistence backend tests (create/list/delete across restarts)
- [ ] ⛔ Cross-owner isolation tests (cannot read/delete other owner’s items)
- [ ] ⛔ UI selection → prompt context injection + attribution appears when used

---

## 12) Final Phase 5.4 Invariant

- [x] ✅ Encoded into design + enforced mechanically at storage-time:

> **“The system can remember what the user approved, without deciding who the user is.”**


---

## Phase 5.4 Completion Note

Phase 5.4 is considered **complete** as a *memory primitive layer*.

This phase intentionally delivers:
- A proposal-before-write memory architecture
- Explicit user approval semantics
- Mechanical guards against identity, clinical, and authoritative language
- Non-use guarantees (delete = not consumed)
- Explicit selection-based retrieval (no auto-recall)
- Owner-scoped, file-backed persistence for development

This phase **does not** include:
- User-facing UI (ledger, approve/decline buttons, forget flows)
- Consent gating or Phase 5.3 integration
- Cross-owner adversarial enforcement
- Prompt injection or downstream application usage

All unchecked items are **intentionally deferred** to Phase 5.5 (Product Integration)
and Phase 5.6 (Safety + Adversarial Hardening).

Invariant achieved:
> “The system can remember what the user approved, without deciding who the user is.”
