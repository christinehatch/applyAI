# Phase 5.5 — Consent UI Copy & Guarantees

## Purpose

This document defines the **exact user-facing language** for consent in Phase 5.5.

It ensures that:
- Consent is understandable without legal or technical framing
- Users know *exactly* what approval and decline do
- No UI wording implies obligation, recommendation, or evaluation
- Consent remains empowering, reversible only via future proposals, and non-retroactive

This document is **authoritative** for all consent-related UI text.

---

## Core Principles for Consent Copy

All consent-related language must follow these principles:

- Plain language (no legal or psychological jargon)
- Neutral tone (no pressure, no recommendation)
- Explicit consequences (what happens if you approve or decline)
- No framing that implies correctness, accuracy, or judgment
- No implication that declining is harmful or inferior

---

## Consent UI Placement

Consent UI text may appear **only** on:

- `/memory/proposals`
- `/memory` (informational copy only)

Consent copy must **never** appear in:
- Conversation flow
- Summaries
- Reflections
- Interpretations

---

## `/memory/proposals` — Proposal Card Copy

### Proposal Header

**Suggested heading:**
> *Memory proposal*

Optional subheading:
> *You’re in control of what gets saved.*

---

### Proposal Body

**Proposed text (verbatim from system):**
> “You often approached the problem by breaking it into parts and thinking about how those pieces fit together before taking action.”

**Context line (static copy):**
> This is a suggestion based on your earlier responses.

---

### Consent Explanation (Required)

This copy must appear **before** the action buttons:

> If you approve this, it will be saved to your memory.
>  
> If you decline, nothing will be saved.

Optional clarifier (recommended):

> You can approve or decline each suggestion independently.

---

## Action Buttons

### Approve Button

**Label:**
> Approve & Save

**Hover / helper text (optional):**
> Saves this to your memory.

**Guarantees communicated by copy:**
- One-time action
- Explicit consent
- Memory is created only after click

---

### Decline Button

**Label:**
> Decline

**Hover / helper text (optional):**
> Does not save anything.

**Guarantees communicated by copy:**
- No penalty
- No memory created
- No future obligation

---

## Post-Action Behavior (Implicit, Not Text)

After approval or decline:
- Proposal disappears from pending list
- No confirmation modal required
- No celebratory or discouraging language
- No undo button (reversibility only via future proposals)

---

## `/memory` Page — Informational Copy

### When Memory Exists

Optional header text:
> Your saved memory

Optional subtext:
> Only items you’ve explicitly approved appear here.

---

### When No Memory Exists

Suggested copy:
> No memory has been saved yet.

Followed by:
> Memories only appear after you explicitly approve them.

---


## Implemented UI Alignment (Step 4)

The following templates implement the consent copy defined above
without modifying protected conversational surfaces:

- `templates/memory.html`
  - Informational-only copy
  - No consent actions
  - No mutation on view

- `templates/memory/proposals.html`
  - Explicit approve / decline explanations
  - Equal-weight action buttons
  - No recommendation or evaluative language
  - All actions routed through POST endpoints


---


## Language That Is Explicitly Forbidden

The following phrases (or equivalents) must **never** appear in consent UI:

- “Recommended”
- “Accurate”
- “Correct”
- “Best fit”
- “Based on psychology”
- “Scientifically validated”
- “Improve your results”
- “Help us help you”
- “Required”
- “You should”

---

## Consent Is Not…

To avoid ambiguity, consent UI must never imply that approval:

- Improves system behavior
- Affects future prompts
- Is required to continue
- Is expected or encouraged
- Is a form of agreement or endorsement

---

## Accessibility & Tone Requirements

- Buttons must be equal visual weight
- Decline must not be visually de-emphasized
- No countdowns, nudges, or urgency framing
- No dark patterns

---

## Relationship to Other Phase 5.5 Documents

This document must align with:

- `phase5_5_consent_state_map.md`  
  → defines what consent *means*

- `phase5_5_route_contracts.md`  
  → defines where consent logic may exist

- `phase5_5_protected_surfaces.md`  
  → defines what must not change

- `phase5_5_diff_plan.md`  
  → defines how consent UI is introduced safely

- `phase5_5_checklist.md`  
  → defines completion criteria

