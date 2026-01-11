# Phase 5.5 — Consent UI Template Mapping

## Purpose

This document maps **approved consent UI copy** (from Step 2) to **specific templates and routes**, while explicitly identifying:

- Which templates may be modified
- Which templates must not be modified
- What kind of changes are allowed (copy-only vs structural)
- Where consent UI must never appear

This document exists to **prevent accidental contamination** of Phase 1–3 behavior.

---

## Guiding Rule

Consent UI is **additive and isolated**.

No existing conversational, reflective, or summary behavior may be altered to support consent.

---

## Templates That MAY Be Modified

### 1. `templates/memory_proposals.html` (or equivalent)

**Purpose of template:**
- Display pending memory proposals
- Allow explicit approve / decline actions

**Allowed changes:**
- Add consent explanatory copy (from `phase5_5_consent_ui_copy.md`)
- Add labels, helper text, or microcopy
- Adjust layout to visually balance Approve / Decline buttons
- Add non-mutating informational text

**Explicitly allowed UI elements:**
- “If you approve this, it will be saved…”
- “If you decline, nothing will be saved…”
- Equal-weight Approve & Decline buttons

**Explicitly forbidden changes:**
- Writing memory directly in template logic
- Calling summary or conversation functions
- Adding conditional logic that infers consent
- Auto-approving or default-selecting options

**Invariant:**
> This template may *display* consent actions but may never *implement* consent logic.

---

### 2. `templates/memory.html`

**Purpose of template:**
- Display approved memory items only

**Allowed changes:**
- Add informational copy:
  - “Only items you’ve explicitly approved appear here.”
  - “Memories only appear after approval.”
- Add a link to `/memory/proposals`

**Explicitly forbidden changes:**
- Displaying pending proposals
- Displaying declined proposals
- Mutating memory on render
- Adding approval or decline actions

**Invariant:**
> This template is strictly read-only.

---

## Templates That MUST NOT Be Modified

### 1. Conversation Templates (Phase 1–3)

Includes (examples):
- `templates/index.html`
- Any prompt, follow-up, or question template

**Must not change:**
- Layout
- Copy
- Control flow
- State transitions

**Reason:**
> Consent must never influence conversational behavior.

---

### 2. Summary / Reflection Templates

Includes:
- Summary output pages
- Reflection or interpretation displays

**Must not change:**
- Content
- Structure
- Trigger conditions

**Reason:**
> Consent is about storage, not interpretation.

---

## Routes That Must Remain Untouched

This document assumes the following routes are **protected surfaces** (see `phase5_5_protected_surfaces.md`):

- `/` (conversation flow)
- Summary generation routes
- Any Phase 1–3 handlers

Consent UI must not introduce:
- Conditional logic
- Flags
- State checks
- Side effects

---

## Where Consent UI Must NEVER Appear

Consent UI copy must not appear in:

- Conversation prompts
- Follow-up questions
- Summaries
- Reflections
- Interpretation output
- Feedback forms

If consent text appears in any of the above, Phase 5.5 is considered violated.

---

## Mapping Summary Table

| Area | Allowed? | Notes |
|----|----|----|
| `/memory/proposals` | ✅ Yes | Primary consent UI |
| `/memory` | ✅ Yes (info only) | Read-only |
| Conversation flow | ❌ No | Protected |
| Summary pages | ❌ No | Protected |
| Reflection output | ❌ No | Protected |

---

## Relationship to Other Phase 5.5 Docs

This document operationalizes:

- `phase5_5_consent_ui_copy.md`
- `phase5_5_route_contracts.md`
- `phase5_5_protected_surfaces.md`

And constrains implementation described in:

- `phase5_5_diff_plan.md`

---

## Exit Criteria for Step 3

Step 3 is complete when:

- All consent UI locations are explicitly mapped
- All protected templates are explicitly named
- No ambiguity remains about *where* consent UI lives
- No code has been modified yet

