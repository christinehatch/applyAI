# Phase 5.5 — Consent State Map

## Purpose

This document defines the **authoritative consent state machine** for Phase 5.5.

It specifies:
- What consent *is* (states and invariants)
- Where consent appears in the product
- How consent gates memory creation
- What consent must **never** do
- How consent integrates with existing Phase 1–3 behavior without modifying it

This document is **behavioral**, not implementation-level.  
All code, tests, and UI must conform to this state map.

---

## Core Invariants

The following invariants must hold at all times:

- Consent is **explicit**, never implied
- Consent is **granular** (proposal-specific)
- Consent is **revocable only via future proposals**, not retroactively
- Consent is **required before memory is written**
- Absence of consent must **block memory creation**
- Declining consent must **not create memory**
- Consent state must be **auditable and deterministic**

No exception paths are allowed.

---

## Consent States

Consent exists per **memory proposal**, not globally.

Each proposal is always in exactly one state:

- `pending` — awaiting explicit user action
- `approved` — user explicitly consented
- `declined` — user explicitly declined

State transitions are one-way and irreversible.

---

## Consent State Transitions

```text
(pending)
   │
   ├── approve ──▶ (approved)
   │                  │
   │                  └── creates exactly one memory item
   │
   └── decline ──▶ (declined)
                      └── creates zero memory items
```
                
                      
## Invalid Transitions

The following state transitions are **explicitly disallowed**:

- approved → pending  
- declined → pending  
- declined → approved  
- approved → declined  

---

## Pages Where Consent Appears

Consent UI may appear **only** on the following pages:

- `/memory/proposals`
- `/memory`

Consent UI must **never** appear on:

- `/` (conversation flow)
- Any Phase 1–3 prompt or follow-up screen
- Any summary page
- Any reflection or interpretation output

---

## Consent UI Behavior by Page

### `/memory/proposals`

- Displays a list of pending proposals
- Each proposal includes:
  - Proposed text
  - Source type
  - Approve button
  - Decline button
- Clicking either button performs a **real route call**
- No memory is written from this page directly

---

### `/memory`

- Displays **only approved memory**
- Does not surface pending or declined proposals
- Does not mutate memory on view
- May include a link to `/memory/proposals`

---

## Enforcement Choke Point

All memory creation **must** occur through:

```http
POST /memory/proposals/<proposal_id>/approve
```

## Single Choke Point

This route is the **single choke point** for:

- Consent validation  
- Memory creation  
- Timestamp assignment  
- Invariant enforcement  

**No other route may create memory.**

---

## Consent Mutation Routes

Consent state may be mutated **only** via:

- `POST /memory/proposals/<id>/approve`
- `POST /memory/proposals/<id>/decline`

No other route may:

- Change proposal state  
- Create memory  
- Modify consent metadata  

---

## Proposal Lifecycle Rules

### Proposal Creation

- Creates a proposal record only  
- Does **not** create memory  
- Sets `decision = pending`  
- Does **not** set `approved_at`  

### Approval

On approval:

- `decision` is set to `approved`  
- `approved_at` is set **exactly once**  
- **Exactly one** memory item is created  
- `memory.created_at == memory.updated_at`  
- Proposal never appears in pending lists again  

### Decline

On decline:

- `decision` is set to `declined`  
- `approved_at` must remain `null`  
- No memory is created  
- Proposal never appears in pending lists again  
- Declined proposals do not reappear unless explicitly re-proposed  

---

## Prohibited Behaviors (Hard Rules)

The following are **never allowed**:

- Creating memory without explicit approval  
- Inferring consent from behavior  
- Bulk approval helpers  
- Auto-approval  
- Retroactive consent  
- Consent logic inside conversation handlers  
- Consent logic inside summary generation  
- Memory writes during reads  
- Timestamp mutation on view  
- Bypassing routes via internal helpers  

**Violations are considered Phase 5.5 failures.**

---

## Relationship to Other Phase 5.5 Documents

This document works in conjunction with:

- **`phase5_5_route_contracts.md`**  
  → defines which routes must not change  

- **`phase5_5_protected_surfaces.md`**  
  → defines code that must remain untouched  

- **`phase5_5_diff_plan.md`**  
  → defines how changes are applied safely  

- **`phase5_5_checklist.md`**  
  → defines completion and exit criteria  
