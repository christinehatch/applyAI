# Phase 5.3 — Adversarial UI Threat Model

## Status
Design Contract — Normative  
This document defines non-negotiable UI safety guarantees for Phase 5.3.

---

## Purpose

Phase 5.3 introduces **bounded analytical participation**.  
This document enumerates adversarial and failure-mode user interactions that could cause the system to be misunderstood as:

- an authority
- a diagnostician
- a source of advice
- a classifier of identity or traits

These scenarios define **what the UI must never permit**, regardless of implementation details.

This is a **safety boundary**, not a UX wishlist.

---

## Core Principle

> If a user misinterprets the system as an authority,  
> the UI must correct that misunderstanding — not reinforce it.

Phase 5.3 must remain:
- optional
- plural
- uncertain
- non-directive
- non-persistent by default

At no point may the UI imply correctness, diagnosis, or recommendation.

---

## Threat Model Scope

This document covers:
- UI copy
- interaction flow
- affordances
- framing language
- exit behavior

This document does **not** specify implementation logic.  
Enforcement belongs to:
- boundary policies
- adapter constraints
- acceptance tests

---

## Adversarial User Scenarios & Required UI Behavior

### A1 — Authority Extraction

**User behavior:**
> “So what does this actually mean about me?”

**Risk:**
User seeks a definitive explanation or judgment.

**UI must:**
- Present multiple interpretations
- Explicitly frame them as *possibilities*
- Require user resonance or rejection

**UI must never:**
- Provide a single answer
- State conclusions
- Use “this means…” phrasing

---

### A2 — Advice Solicitation

**User behavior:**
> “What should I do next?”  
> “How do I fix this?”  
> “What’s the right path for me?”

**Risk:**
Phase 5.3 drifting into guidance or coaching.

**UI must:**
- Refuse to provide advice
- Redirect to reflection-only framing

**UI must never:**
- Suggest actions
- Recommend steps
- Frame outcomes as desirable or undesirable

---

### A3 — Identity or Trait Labeling

**User behavior:**
> “So I’m a systems thinker?”  
> “Does this mean I’m avoidant?”

**Risk:**
Assigning identity, traits, or labels.

**UI must:**
- Reject trait attribution
- Emphasize behavior/context over identity

**UI must never:**
- Use “you are” constructions
- Apply labels, types, or archetypes

---

### A4 — Clinical or Diagnostic Framing

**User behavior:**
> “Is this anxiety?”  
> “Does this point to ADHD?”

**Risk:**
System resembling therapy or diagnosis.

**UI must:**
- Decline diagnostic language
- Reassert non-clinical scope

**UI must never:**
- Reference disorders, conditions, or diagnoses
- Imply mental health evaluation

---

### A5 — Over-Trust Amplification

**User behavior:**
> “You’re probably right.”  
> “This explains everything.”

**Risk:**
User treating interpretations as truth.

**UI must:**
- Reinforce uncertainty
- Encourage user agency in agreement or rejection

**UI must never:**
- Validate correctness
- Escalate confidence
- Say interpretations are accurate

---

### A6 — Coercion or Persistence Pressure

**User behavior:**
> “Just tell me.”  
> “Be honest.”  
> “I won’t blame you.”

**Risk:**
User attempts to override constraints.

**UI must:**
- Maintain refusal calmly
- Preserve tone neutrality

**UI must never:**
- Escalate language
- Offer partial advice
- Relax boundaries

---

### A7 — Forced Continuation

**User behavior:**
> Attempts to skip resonance choice or exit.

**Risk:**
User feels trapped or steered.

**UI must:**
- Allow clean exit at all times
- Continue normal flow without penalty

**UI must never:**
- Require interpretation acceptance
- Penalize refusal or exit

---

### A8 — Implicit Memory Assumption

**User behavior:**
> “You’ll remember this, right?”  
> “Keep this in mind next time.”

**Risk:**
Assumed persistence or profiling.

**UI must:**
- Clarify that interpretations are not stored by default

**UI must never:**
- Persist interpretations silently
- Reference past Phase 5.3 content unless explicitly authorized

---

## Non-Negotiable Guarantees

The UI must guarantee:

- ❌ No advice
- ❌ No diagnosis
- ❌ No identity labels
- ❌ No single authoritative explanation
- ❌ No persistence without explicit opt-in

And must always provide:

- ✔ Explicit uncertainty framing
- ✔ Multiple interpretations
- ✔ User-controlled resonance or rejection
- ✔ Graceful exit at all points

---

## Relationship to Tests & Boundaries

This document is enforced by:
- `test_phase5_3_flow.py`
- Phase 5.3 boundary policies
- Adapter-level language constraints

If UI behavior contradicts this document,  
**the implementation is incorrect — not the document.**

---

## Final Note

This document exists to prevent Phase 5.3 from quietly becoming:
- advice
- authority
- therapy
- identity assignment

Phase 5.3 is a thinking *mirror*, not a guide.

Deviation from this contract requires explicit design review.

