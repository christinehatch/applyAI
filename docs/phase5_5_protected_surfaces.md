# Phase 5.5 — Protected Routes & Code Surfaces

**Purpose**  
This document defines the routes, functions, and storage semantics that **must not change** as Phase 5.5 is implemented.

Phase 5.5 may *extend* behavior via UI, documentation, and opt-in flows — but must not alter existing logic, side effects, or invariants.

If a proposed feature requires violating this document, it is **not Phase 5.5**.

---

## 🔒 Global Invariants (Apply Everywhere)

Phase 5.5 code **must not**:

- Write memory without explicit user approval
- Infer consent from navigation, UI state, or completion
- Modify timestamps retroactively
- Introduce identity labels, traits, scores, or diagnoses
- Add side effects to `GET` routes
- Persist conversation state

---

## 1. `/` — Conversation Driver Route

**Status:** ❌ DO NOT CHANGE BEHAVIOR

### What this route does
- Accepts user input
- Advances `conversation_state["stage"]`
- Appends responses to `conversation_state["responses"]`
- Renders the next prompt or summary

### 🔒 Must NOT change
- Prompt sequence logic
- Stage advancement rules
- Response storage structure
- Cookie / owner initialization behavior

### ✅ Allowed in Phase 5.5
- Reading `conversation_state`
- Triggering summary generation *after* conversation completion
- UI-only additions (banners, notices, links)

### ❌ Forbidden
- Auto-triggering memory approval
- Writing memory or proposals here
- Consent logic embedded in this route

**Rationale:**  
This route defines the cognitive mirror. Altering it invalidates all downstream interpretation.

---

## 2. `generate_summary(...)`

**Status:** ❌ LOGIC LOCKED

### What it does
- Converts collected responses into reflective summary text
- Emits **memory proposals** (not memory)
- Returns summary output

### 🔒 Must NOT change
- When it runs (only after sufficient responses)
- That it produces *proposals*, not memory
- Idempotency (safe to call multiple times)
- No timestamps written here

### ✅ Allowed
- Attaching metadata to proposals
- Adding `source_type`
- Read-only logging

### ❌ Forbidden
- Writing to memory storage
- Applying approval / decline logic
- Auto-accepting proposals

**Invariant:**  
`generate_summary()` must remain a pure **reflection → proposal** transformer.

---

## 3. `/memory` — Memory Viewer

**Status:** ❌ READ-ONLY FOREVER

### What it does
- Displays **approved memory only**
- Never shows pending or declined proposals

### 🔒 Must NOT change
- Filtering logic (`approved` only)
- No side effects
- No proposal mutation

### ✅ Allowed
- UI layout changes
- Copy changes
- Sorting or grouping

### ❌ Forbidden
- Approve / decline actions
- Timestamp mutation
- Editing memory content

**Invariant:**  
`/memory` must always be safe to load without consent consequences.

---

## 4. `/memory/proposals` — Proposal Viewer

**Status:** ⚠️ SEMI-LOCKED (UI ONLY)

### What it does
- Lists pending proposals
- Displays approve / decline actions

### 🔒 Must NOT change
- Proposal loading logic
- Decision state machine
- No memory writes

### ✅ Allowed
- UI text and layout
- Consent explanations
- Warnings and affordances

### ❌ Forbidden
- Bulk actions
- Auto-decision
- Time-based expiration

---

## 5. `/memory/proposals/<id>/approve`

**Status:** 🔒 CRITICAL — INVARIANTS LOCKED

### What it must always do
- Set `decision = "approved"`
- Set `approved_at = now`
- Create **exactly one** memory entry
- Enforce:
  - `memory.created_at == approved_at`
  - `memory.updated_at == approved_at`

### 🔒 Must NOT change
- Timestamp equality invariant
- One proposal → one memory rule
- Proposal text integrity
- No delayed writes

### ❌ Forbidden
- Editing memory after creation
- Adding metadata post-approval
- Background jobs

**Note:**  
This behavior is enforced by automated tests and must remain invariant.

---

## 6. `/memory/proposals/<id>/decline`

**Status:** 🔒 LOGIC LOCKED

### What it must do
- Set `decision = "declined"`
- Optionally set `declined_at`
- Never create memory

### 🔒 Must NOT change
- No memory creation
- No memory timestamps
- No reconsideration logic

### ✅ Allowed
- Optional decline reason (string)
- UI messaging

---

## 7. Memory Storage Layer (`memory/storage.py`)

**Status:** 🔒 WRITE-SEMANTICS LOCKED

### Functions with locked behavior
- `load_proposals(owner_id)`
- `load_memory(owner_id)`
- `approve_proposal(...)`
- `decline_proposal(...)`

### 🔒 Must NOT change
- Storage format
- Timestamp semantics
- Decision state machine
- Append-only behavior

### ✅ Allowed
- Read helpers
- Indexes
- Analytics *outside* storage layer

---

## 8. Conversation State (`conversation_state`)

**Status:** ❌ STRUCTURAL LOCK

### Must remain
- Ephemeral
- Session-scoped
- Non-persistent

### ❌ Forbidden
- Writing memory here
- Storing consent decisions here
- Identity or profile fields

---

## 🚫 Explicitly Forbidden Additions (Phase 5.5)

The following must **not** exist in Phase 5.5:

- `/memory/approve_all`
- `/memory/auto_approve`
- `/profile`
- `/assessment`
- `/scores`
- `/traits`
- `/recommend_jobs`
- `/export_for_employer`

If required, these belong to a **future phase with new contracts**.

---

## Final Guarantee

Phase 5.5 guarantees:

> No user data is stored, inferred, labeled, or shared  
> without an explicit, visible, reversible user action.

---

## Next Planned Documents
- `docs/phase5_5_consent_ui.md`
- `docs/phase5_5_ui_states.md`
- `docs/phase5_5_non_goals.md`

