# Phase 5.5 — Consent UI Design

## Purpose

Design a consent experience that is:

* Explicit (no implied consent)
* Time-scoped
* Reversible
* Non-coercive
* Fully auditable by the user

This document specifies **UI states and copy**, not implementation logic. Behavior is governed by `phase5_5_route_contracts.md`.

---

## Guiding Principles

1. **No silent defaults**

   * Consent always starts OFF
   * No pre-checked boxes

2. **Consent ≠ Memory**

   * Granting consent does not save memory
   * Memory still requires proposal + approval

3. **Granularity**

   * Consent applies to *capabilities*, not identity or traits

4. **Reversibility**

   * Revoking consent takes effect immediately
   * Revocation does not retroactively delete memory

5. **Non-authoritative tone**

   * The UI never implies benefit, improvement, or correctness

---

## Consent Entry Points

Consent UI may be shown **only** at the following times:

1. When the user explicitly requests deeper analysis or interpretation
2. When the user navigates to the Memory or Ledger section
3. When the user opens Settings → AI Participation

Consent is **never** shown mid-response.

---

## Consent States

### State A: No Consent (Default)

**Visual**

* Status badge: `AI reasoning: Off`
* Subtext: `Reflections only`

**Available actions**

* Continue without consent
* Learn what consent enables

**Copy (example)**

> You’re currently using reflection-only mode.
> No AI reasoning or interpretation is active.

---

### State B: Consent Explanation

**Purpose**
Explain *what changes* if consent is granted — without persuasion.

**Must include**

* What AI *can* do
* What AI *cannot* do
* What does NOT change

**Copy (example)**

> If you enable AI-assisted reasoning:
>
> * The system may help summarize or connect ideas you’ve shared
> * It will not diagnose, label, or evaluate you
> * It will not save memory without approval
> * You can turn this off at any time

Buttons:

* `Enable AI-assisted reasoning`
* `Keep reflection-only mode`

---

### State C: Consent Granted

**Visual**

* Status badge: `AI reasoning: On`
* Timestamp shown: `Enabled at {time}`

**Available actions**

* Revoke consent
* View memory ledger

**Copy (example)**

> AI-assisted reasoning is currently enabled.
> You can disable this at any time.

---

### State D: Consent Revoked

**Behavior**

* Takes effect immediately
* Active session downgrades to reflection-only

**Copy (example)**

> AI-assisted reasoning has been turned off.
> Existing memory is unchanged.

---

## Time Scope

Consent is scoped to:

* The current session OR
* A user-selected duration (e.g. `this session`, `today`, `until revoked`)

Default: **this session only**

---

## Explicit Non-Features

The consent UI must never:

* Suggest outcomes or benefits
* Rank or score the user
* Use psychological or clinical language
* Bundle consent with memory approval
* Hide revocation behind multiple steps

---

## Relationship to Memory Ledger

* Memory proposals may appear regardless of consent state
* Approval UI is separate and unaffected
* Ledger always reflects the truth

---

## Success Criteria

This UI is correct if:

* A user can use the system fully without consenting
* A user can audit exactly what was enabled and when
* Revocation feels safe and immediate
* No user could reasonably say "I didn’t realize what I agreed to"

---

*End of Phase 5.5 Consent UI Design*

