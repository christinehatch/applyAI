# Phase 5.5 Diff Plan — Consent UI

## Goal
Introduce explicit user consent for memory persistence
without modifying conversation flow, signals, or summaries.

---

## Files Allowed to Change

### templates/memory_proposals.html
Allowed:
- Add consent explanation text
- Adjust button labels or placement
- Visual-only changes

Forbidden:
- Adding hidden form fields
- Adding default-checked inputs
- Triggering automatic approval

---

### app.py (memory proposal routes only)
Allowed:
- Minimal guards inside:
  - /memory/proposals/<id>/approve
  - /memory/proposals/<id>/decline

Forbidden:
- Changes to conversation handlers
- Changes to summary generation
- Changes to proposal creation
- New global state
- Consent flags stored in session or memory

---

## Files That Must Not Change

- app.py conversation routes
- signal detection
- reflection logic
- generate_summary()
- proposal creation logic
- memory storage schema

Any diff here is a hard stop.

---

## Tests That Must Pass

- Deterministic test agent:
  - Approval creates exactly one memory
  - Decline creates zero memory
  - Timestamp invariants hold
  - No side effects on repeated runs

---

## Non-Goals

- No psychological consent modeling
- No background consent flags
- No one-time global consent
- No interpretation consent

Consent applies only to memory persistence.

---

## Review Rule

If `git diff` shows changes outside this plan,
the change must be reverted or the plan amended *first*.

