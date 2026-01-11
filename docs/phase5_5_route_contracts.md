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
* Emit *memory proposals* during summary generation (Phase 5.4)

**Explicitly Forbidden**:

* Writing to memory storage
* Assigning interpretations as fact
* Persisting inferred attributes

**Invariants**:

* Conversation must be replayable deterministically
* No memory creation without `/memory/proposals/*/approve`

---

## Route: `/summary` (Implicit via `/` completion)

**Purpose**:

* Generate reflective summary text
* Emit memory proposals (not memory)

**Allowed**:

* Generate reflection language
* Append proposals via `append_proposal()`

**Explicitly Forbidden**:

* Writing to memory store
* Editing or deleting proposals

**Invariants**:

* Proposal emission must be idempotent per session
* Proposal text must pass `validate_memory_text()` before approval
* Re-running summary generation must not duplicate proposals

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

## Route: `/reset`

**Purpose**:

* Reset conversation state

**Allowed**:

* Clear in-memory conversation state

**Explicitly Forbidden**:

* Deleting memory
* Deleting proposals

**Invariants**:

* Memory persists across resets

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

