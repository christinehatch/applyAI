# Phase 5.5 Route Contracts

> **Purpose**: Freeze behavioral guarantees before any consent UI or additional logic is introduced.
> These contracts define what each route *is allowed* and *not allowed* to do.
>
> Guiding principle: **UI may evolve; behavior must not drift.**

---

## Step 0 — Immutability Lock

As of Phase 5.5, the following are considered **behaviorally frozen**.
Any change to these surfaces requires:
- a new phase number
- a new route contract
- and new tests

Refactors, cleanups, and “minor improvements” are NOT permitted.


## Global Phase 5 Invariants (Apply to ALL routes)

* No route may:

  * Assign identity labels, traits, or diagnoses
  * Store inferred psychological attributes
  * Modify memory without explicit user action
  * Create memory as a side-effect of rendering or summarization

* Memory rules:

  * Memory is **proposal → explicit approval → immutable record**
  * Approved memory must be append-only
  * Declined memory must never be persisted as memory

* Consent rules:

  * Consent is **opt-in**, **session-scoped**, and **revocable**
  * Lack of consent must never degrade the core experience
  
* Timestamp rules:

  * All timestamps are server-generated
  * Client input must never influence timestamps
  
  
  ---
  

## Consent UI Clarifications (Phase 5.5)

**Purpose**:
Define how consent-related UI may interact with existing routes without altering behavior.

**Rules**:

* Consent UI must:
  * Be a thin client over existing routes
  * Never introduce new side effects
  * Never bypass route-level invariants

* Consent UI may:
  * Explain consequences of approval or decline
  * Delay user action
  * Offer contextual reminders about consent

* Consent UI must NOT:
  * Auto-trigger `/approve` or `/decline`
  * Pre-select consent choices
  * Infer consent from interaction or inactivity
  * Change proposal contents

**Invariant**:
> All consent decisions must remain explicit, user-initiated, and route-driven.


---

## Route: `/` (Conversation Engine)

**Purpose**:

* Drive the structured, multi-stage reflective conversation

**Allowed**:

* Accept user input
* Advance stages deterministically
* Log conversation events (internal only)
* Record reflections for an optional, user-initiated memory offer (proposals are emitted only by `POST /memory/opt-in`)

**Explicitly Forbidden**:

* Writing to memory storage
* Assigning interpretations as fact
* Persisting inferred attributes

**Invariants**:

* Conversation must be replayable deterministically
* No memory creation without `/memory/proposals/*/approve`
* No proposal creation without `/memory/opt-in`

---

## Route: `/summary` (Implicit via `/` completion)

> **Changed in Phase 5.4 completion:** the summary no longer emits proposals.
> It only records which reflections *could* be proposed. Emission moved to
> `POST /memory/opt-in` so memory is opt-in and ordered after reflection.

**Purpose**:

* Generate reflective summary text
* Record this conversation's reflections in session state (`summary_reflections`)
* Offer an explicit, skippable "Review as memory proposals" action

**Allowed**:

* Generate reflection language
* Set `summary_ready` and `summary_reflections` in the owner's conversation state

**Explicitly Forbidden**:

* Writing to memory store
* Appending, editing, or deleting proposals
* Pre-selecting or auto-submitting the memory offer

**Invariants**:

* Rendering the summary creates no proposals and no memory
* Re-running summary generation has no storage side effects

---

## Route: `/memory/opt-in` (POST)

**Purpose**:

* Explicit user request to review this conversation's reflections as memory proposals

**Allowed**:

* Append one `SELF_OBSERVATION` proposal per recorded reflection via `append_proposal()`
* Set `memory_opt_in` and `proposals_emitted` in the owner's conversation state

**Explicitly Forbidden**:

* Writing to memory store
* Reading or setting `phase5_consent_token` (memory consent is separate from Phase 5 consent)
* Running before the summary exists

**Invariants**:

* Returns 409 and writes nothing if `summary_ready` is false
* Idempotent per conversation: a replay creates no duplicate proposals
* Proposal text must pass `validate_memory_text()` before approval

---

## Route: `/memory`

**Purpose**:

* Display approved memory items only

**Allowed**:

* Read-only display of active memory
* Show timestamps and metadata

**Explicitly Forbidden**:

* Editing memory
* Creating memory
* Showing declined or pending proposals

**Invariants**:

* Memory displayed must exactly match stored records
* Timestamps are authoritative

---

## Route: `/memory/proposals`

**Purpose**:

* Display pending memory proposals

**Allowed**:

* List proposals with status = `pending`
* Show proposal metadata

**Explicitly Forbidden**:

* Editing proposal text
* Auto-approving or auto-declining

**Invariants**:

* Proposals must remain visible until explicitly resolved

---

## Route: `/memory/proposals/<id>/approve` (POST)

**Purpose**:

* Convert a proposal into an approved memory item

**Allowed**:

* Validate proposal text
* Write a new memory record
* Mark proposal as approved

**Explicitly Forbidden**:

* Modifying existing memory
* Editing proposal text

**Invariants**:

* `created_at == updated_at` on creation
* Memory record is immutable after creation
* Exactly one memory record per approved proposal

---

## Route: `/memory/proposals/<id>/decline` (POST)

**Purpose**:

* Explicitly reject a memory proposal

**Allowed**:

* Mark proposal as declined
* Store optional decline reason
* Clear the proposal text (decline must not retain usable text)

**Explicitly Forbidden**:

* Writing to memory store
* Creating timestamps implying memory creation

**Invariants**:

* Declined proposals never appear in `/memory`
* Declined proposals must not have `approved_at`

---

## Route: `/memory/<id>/forget` (POST)

**Purpose**:

* Allow user to delete an approved memory

**Allowed**:

* Soft-delete memory record
* Preserve audit trail

**Explicitly Forbidden**:

* Hard deletion
* Cascade effects on other memory

**Invariants**:

* Deleted memory is excluded from `/memory`
* Deleted memory remains inspectable internally

---

## Route: `/memory/select` (GET, POST)

**Purpose**:

* Let the user choose which approved memory items may be used in this conversation
* Show exactly what is in use, with the attribution line

**Allowed**:

* Store selected ids in the owner's conversation state (`selected_memory_ids`)
* Resolve context only via `build_selected_memory_context()`

**Explicitly Forbidden**:

* Writing selection to disk
* Selecting ids that are deleted, unknown, or owned by someone else (silently dropped)
* Pre-selecting items the user has not chosen in this conversation

**Invariants**:

* Empty selection → empty context and no attribution line
* `build_selected_memory_context()` is the only path by which memory reaches any downstream use

---

## Route: `/memory/select/clear` (POST)

**Purpose**:

* Stop using all selected memory in this conversation

**Invariants**:

* Clears `selected_memory_ids` only; memory items are unchanged

---

## Route: `/reset`

**Purpose**:

* Reset conversation state

**Allowed**:

* Clear the caller's in-memory conversation state, including memory selection

**Explicitly Forbidden**:

* Deleting memory
* Deleting proposals

**Invariants**:

* Memory persists across resets
* Other owners' conversations are untouched
* Phase 6 role context (`role_context`) is cleared, since the state is replaced

---

## Non-Routes (Must Never Exist)

* Bulk memory approval
* Automatic proposal approval
* Memory editing endpoints
* Psychological scoring endpoints
* Cross-user memory access

---

## Final Design Constraint

> **Any future feature must prove it does not violate these contracts.**

UI, analytics, monetization, and partnerships must layer *on top of* this foundation — never through it.

