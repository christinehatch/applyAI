# Phase 5.4 — Memory Schema & Invariants

> **Purpose**
> Define the *minimum* data model and mechanical invariants for Phase 5.4 (Longitudinal Awareness), such that memory can exist **without identity imposition**, **without hidden inference**, and **without application leakage** (Phase 6 remains out of scope).

---

## Phase 5.4 Core Question

**Can insight persist without identity being imposed?**

---

## Scope

### In scope

* Optional, opt-in memory
* Proposal → user edit → approve/decline (no automatic writes)
* User-visible ledger with provenance (what / when / where it came from)
* Explicit forgetting controls
* Retrieval only via **explicit user selection**

### Out of scope (must not be implemented in Phase 5.4)

* Project suggestions, role suggestions, career planning, resume/portfolio formatting
* Memory influencing signal detection, Phase 3 reflection language, follow-up selection, or Phase 5.3 gating
* “Implicit” or “helpful” auto-recall (any silent enrichment)

---

## Design Principles (Non-Negotiable)

1. **Proposal-before-write:** Nothing is stored unless user approves it.
2. **Verbatim storage:** The system stores exactly what the user approved.
3. **No identity locking:** Memory cannot become a trait label.
4. **No hidden inference:** Only user-authored or user-edited content is eligible.
5. **No auto-consumption:** Memory is never used unless the user explicitly selects it.
6. **Forgetting means non-use:** Deleted items are not retrievable or used again.

---

## Entity: MemoryItem (Stored Ledger Entry)

A MemoryItem exists **only** after user approval.

### Required fields

* **id**: string (unique identifier)
* **owner_id**: string (required; per-user isolation; do not rely on global state)
* **text**: string (exact wording approved by the user; displayed verbatim)
* **kind**: MemoryKind (allowlist enum; see below)
* **source**: MemorySource (provenance; see below)
* **created_at**: datetime
* **updated_at**: datetime
* **status**: `"active"` | `"deleted"`
* **deleted_at**: datetime | null

### MemoryKind (allowlist)

Only these kinds are allowed in Phase 5.4:

* **PREFERENCE**: “I prefer…”
* **CONSTRAINT**: “I can’t / won’t…”
* **GOAL**: “I want to…”
* **SELF_OBSERVATION**: user-endorsed “I’ve noticed…” phrasing (non-identity-locking)

> **Important:** This allowlist is a structural defense against “inferred trait memory.”

---

## Entity: MemoryProposal (Pre-Approval Workflow)

A MemoryProposal is how memory is offered, edited, and approved/declined.

### Required fields

* **proposal_id**: string (unique identifier)
* **owner_id**: string
* **proposed_text**: string (verbatim candidate text shown to user)
* **kind**: MemoryKind
* **source**: MemorySource
* **created_at**: datetime
* **decision**: `"pending"` | `"approved"` | `"declined"`
* **decided_at**: datetime | null
* **final_text**: string | null (the user-edited version that is approved)
* **result_memory_id**: string | null (set only when approved)

### Notes

* Approving creates a MemoryItem from **final_text**.
* Declining must have **no side effects** (see invariants).

---

## Entity: MemorySource (Provenance)

Memory must be attributable to a visible moment in the system.

### Required fields

* **source_type**: `"phase3_reflection"` | `"phase5_3_interpretation"`
* **source_id**: string | null (optional pointer to a reflection/interpretation artifact)
* **note**: string | null (human-readable, e.g., “After Phase 3 summary”)

### Prohibited in provenance

* Signal names
* Scores
* Classifications
* Hidden model outputs not shown to the user

---

## Ephemeral: SelectedMemoryContext (Retrieval Guard)

This structure is never persisted. It exists only to build request context when the user explicitly selects memory items.

### Required fields

* **selected_memory_ids**: list of string
* **resolved_texts**: list of string (the corresponding MemoryItem.text values)
* **attribution_line**: string (must be: “Using the items you selected…”)

### Hard rule

If `selected_memory_ids` is empty, memory context is empty.

---

## Mechanical Invariants (Must Be Enforced + Tested)

### Invariant A — Proposal-before-write

A MemoryItem may be created **only** from an approved MemoryProposal:

* `proposal.decision == "approved"`
* `proposal.final_text` is present
* `proposal.owner_id == item.owner_id`

### Invariant B — Verbatim ledger

The ledger must display exactly `MemoryItem.text` (no rephrasing at display time).

### Invariant C — Content safety validation on final_text

Before creating a MemoryItem, `final_text` must pass a validator that enforces:

* No identity-locking phrasing (“you are X”, “the kind of person who…”, etc.)
* No clinical/diagnostic language
* No authoritative framing (“definitely”, “this proves…”, etc.)
* No inferred traits (enforced by allowlist + phrasing constraints)

> **Note:** The validator runs on the *memory text being stored*, not on user input.

### Invariant D — Decline has no side effects

If `proposal.decision == "declined"`:

* No MemoryItem is created
* No hidden record stores the declined text for later use

(If auditability is ever required, store only decision metadata—never the declined text.)

### Invariant E — Forget means non-use

If `item.status == "deleted"`:

* It must not appear in the ledger list
* It must not be resolvable into SelectedMemoryContext
* It must not appear in any prompt context

### Invariant F — No auto-consumption

Memory may only influence a response if:

* the user explicitly selected memory IDs, and
* those IDs are passed into context construction, and
* the response includes the attribution line

### Invariant G — Memory does not alter Phase 3 / Phase 5 behavior

Memory must never be used as an input to:

* signal detection
* Phase 3 reflection generation or phrasing
* follow-up selection logic
* Phase 5.3 interpretation request gating

---

## Minimal Service Interfaces (Implementation Targets)

### MemoryStore (persistence)

* list(owner_id) → list of MemoryItem (active only)
* get(owner_id, memory_id) → MemoryItem | null
* create_from_approved_proposal(proposal) → MemoryItem
* delete(owner_id, memory_id) → void

### MemoryProposalService (workflow)

* propose(owner_id, proposed_text, kind, source) → MemoryProposal
* approve(owner_id, proposal_id, final_text) → MemoryItem
* decline(owner_id, proposal_id) → void

### MemorySelectionContextBuilder (retrieval guard)

* build(owner_id, selected_memory_ids) → SelectedMemoryContext

---

## Minimum Test Set (Phase 5.4)

At minimum, Phase 5.4 should ship with tests for:

1. **proposal-before-write** (no MemoryItem created without approved proposal)
2. **decline-no-side-effects** (decline does not create or retain usable text)
3. **delete-non-use** (deleted items excluded from list and context)
4. **validator enforcement** (identity/clinical/authoritative blocks)
5. **no auto-consumption** (no selected IDs → empty context)

---

## Final Invariant (Phase 5.4)

If this is ever false, Phase 5.4 is broken:

> **“The system can remember what the user approved, without deciding who the user is.”**

