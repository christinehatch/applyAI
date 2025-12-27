# Phase 5.3 — Adapter Responsibility Checklist
## Bounded Analytical Participation (Non-Authoritative)

---

## Purpose

This document defines the **exact responsibilities and constraints of Phase 5.3 adapters**.

Adapters are the *only* components allowed to produce analytical language in Phase 5.3.
They are **explicitly subordinate** to the Phase 5 boundary and must never expand capability beyond what is permitted here.

This checklist is enforceable via:
- `tests/test_phase5_3_flow.py`
- Boundary policy enforcement
- Adapter-level unit tests

Adapters **must comply with every item below**.

---

## Core Principle

> Adapters may **offer possibilities**,  
> never **assert conclusions**,  
> never **recommend actions**,  
> and never **define the user**.

---

## 1. Trigger Preconditions (Adapter Must Assume Boundary Has Verified)

Adapters must assume **all** of the following are already true:

- Phase 3 reflection has completed
- Phase 5 consent token is present and valid
- Phase 5.3 has been explicitly requested by the user
- Phase ordering has been enforced by the boundary

Adapters **must not** re-check these conditions — they must trust the boundary.

---

## 2. Interpretation Count (Bounded Range)

Adapters **must** generate:

- **At least 2 interpretations**
- **No more than a bounded maximum** (default: 4)

Rules:
- The exact number may vary
- The adapter must never return a single interpretation
- The adapter must never imply completeness or exhaustiveness

❌ Disallowed:
- “The reason is…”
- “This means that…”
- “The pattern here is…”

✅ Required framing:
- “One possible way to read this…”
- “Another interpretation could be…”
- “It’s also possible that…”

---

## 3. Interpretation Structure

Each interpretation **must**:

- Be self-contained
- Be phrased as *tentative*
- Avoid causal certainty
- Avoid psychological labeling

Each interpretation **must not**:

- Reference signal names
- Reference internal counts
- Reference system detection logic
- Reference prior users or datasets

---

## 4. Uncertainty & Optionality Language (Mandatory)

Adapters **must explicitly state uncertainty**.

Required characteristics:
- Use modal verbs (`may`, `might`, `could`)
- Use observational framing (`appears`, `seems`)
- Include a reminder that interpretations are optional

❌ Forbidden:
- Definitive language
- Confidence scoring
- Ranking interpretations by correctness

---

## 5. User Resonance Requirement

Adapters **must require** the user to choose one of:

- “This resonates”
- “This partially resonates”
- “This does not resonate”

Adapters **must not**:
- Assume agreement
- Advance the conversation without explicit user input
- Interpret silence as acceptance

---

## 6. Absolute Prohibitions (Adapter-Level)

Adapters must never generate:

### ❌ Recommendations
- No advice
- No next steps
- No suggestions
- No “you might want to…”

### ❌ Identity or Trait Labels
- No “you are…”
- No “this shows you’re a…”
- No personality or cognitive typing

### ❌ Clinical or Diagnostic Language
- No mental health terms
- No therapeutic framing
- No diagnostic implications

---

## 7. Exit & Refusal Handling

Adapters **must support graceful exit**.

If the user:
- Declines all interpretations
- Expresses discomfort
- Requests to stop

Then the adapter must:
- Acknowledge the choice neutrally
- Exit Phase 5.3 immediately
- Produce no further interpretation content

---

## 8. Non-Persistence Guarantee

Adapters **must not**:

- Store interpretations
- Modify conversation state
- Affect signal counts
- Feed results back into detection logic

All Phase 5.3 output is:
- Ephemeral
- Session-scoped
- Non-memory-bearing by default

---

## 9. Adapter Failure Conditions

Adapters must fail (not degrade) if:

- Asked to provide advice
- Asked to choose a “best” interpretation
- Asked to define what something “means”
- Asked to continue without user resonance input

Failure must defer to the boundary.

---

## Summary

Adapters are **constrained participants**, not thinkers, judges, or guides.

Their role is to:
- Offer bounded possibilities
- Preserve user agency
- Avoid authority
- Exit cleanly

Anything beyond this is a **Phase 5.3 violation**.

