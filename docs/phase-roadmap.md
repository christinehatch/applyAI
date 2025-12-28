> ⚠️ This document intentionally describes future phases.
> It exists to prevent accidental scope creep while implementing Phase 5.4.
> Nothing in Phase 6 should be implemented until Phase 5.4 is complete and hardened.


# System Roadmap & Phase Design Notes

> **Purpose of this document**
> This document exists to *freeze* the conceptual design decisions discussed so far, so Phase 5.4 can be implemented without accidentally collapsing future possibilities. It is a memory aid, a design guardrail, and a credibility artifact.

---

## 1. Current State (Ground Truth)

### Phase 5.3 — Bounded Analytical Participation (✅ Completed)

**Core question answered:**

> *Can AI participate as a thinking partner without becoming an authority?*

**Guarantees enforced:**

* Explicit user consent
* Explicit user request for interpretation
* Phase ordering (only after Phase 3 reflection)
* Multiple possible interpretations (never a single conclusion)
* Explicit uncertainty framing
* No recommendations
* No job advice
* No conclusions
* No identity locking (no “you are X”)
* No clinical or diagnostic language
* User must choose resonance (resonates / partially / does not)
* No persistence or signal feedback by default

**Mechanisms:**

* Strict LLM boundary
* BoundedInterpretationAdapter
* Mechanical phrase constraints
* Acceptance tests currently passing

Phase 5.3 is considered *ethically closed and stable*.

---

## 2. Phase 5.4 — Longitudinal Awareness (🔒 Next, High-Risk)

**Core question:**

> *Can insight persist without identity being imposed?*

### Scope of Phase 5.4

Phase 5.4 is **only about persistence**, not application.

**Allowed:**

* Optional, opt-in memory
* User-visible memory ledger
* Explicit per-item approval
* Explicit forgetting controls
* Memory phrased in non-identity-locking language

**Explicitly disallowed:**

* Memory influencing signal detection
* Memory influencing interpretation thresholds
* Memory auto-feeding application logic
* Identity crystallization via accumulated traits

**Key invariant:**

> Memory stores *materials*, not conclusions.

Phase 5.4 must be completed and hardened before any applied or career-related functionality is enabled.

---

## 3. Phase 6 — Applied Exploration (🚧 Future Phase, Frozen Conceptually)

Phase 6 is intentionally **not implemented yet**. This section exists to preserve the design so Phase 5.4 does not block it.

### Phase 6 Core Question

> *Can insight be applied without turning the system into an authority or oracle?*

Phase 6 is **explicitly mode-switched, opt-in, and non-default**.

---

## 4. Discovery Entry (Phase 6 On-Ramp)

Discovery Entry supports users who:

* feel lost
* feel overwhelmed
* don’t know what they want
* don’t know what they’re good at

### Discovery Entry Guarantees

* Uncertainty is treated as a valid state, not a deficit
* The system never assigns identity
* The system never prescribes outcomes
* The system never rushes convergence

### Allowed actions in Discovery Entry

* Ask grounding, non-diagnostic questions
* Reflect patterns the *user has already seen*
* Surface categories of work (not prescriptive roles)
* Propose projects as **exploration tools**, not credentials

### Disallowed actions

* “You should be a X”
* Job guarantees or predictions
* Ranking or optimization language
* Resume framing

**Key invariant:**

> At every point, the user can pause, disagree, or walk away without losing authorship.

---

## 5. Phase 6.0 — Applied Exploration (Goal-Oriented or Discovery-Based)

Phase 6.0 supports two valid entry paths:

### Path A — Goal Declared

User says:

> “Getting X job is my goal. Here’s my education and experience.”

System may:

* Decompose the role into observable capabilities
* Propose **project concepts** that demonstrate those capabilities
* Explain tradeoffs and limitations

System must:

* State it cannot guarantee outcomes
* Avoid claims of sufficiency or optimality

---

### Path B — Discovery-Based

User says:

> “I don’t know what I want. Help me find options.”

System may:

* Surface role *families* or problem spaces
* Propose exploratory projects to test interest and energy
* Keep all options open and non-ranked

---

## 6. Phase 6.1 — Career Formatting Mode (Explicit Sub-Mode)

This mode is **only activated when the user explicitly asks**.

### Purpose

* Translate completed work into resume / portfolio language
* Formatting only — no new inference

### Guarantees

* Clear mode switch banner
* Transparent tradeoffs (what clarity removes)
* No job targeting logic
* No predictions

---

## 7. Memory Interaction Rule (Phase 5.4 → Phase 6)

* Phase 6 may **only** use memory items that the user explicitly selects
* Memory is never auto-consumed
* All memory usage is attributable (“using items you selected”)

> Phase 5.4 stores raw materials.
> Phase 6 assembles artifacts — only when asked.

---

## 8. Pressure-Test Summary (Hard Cases)

The system has been tested conceptually against:

* Desperate users seeking authority
* Users with low self-belief
* Users demanding guarantees
* Users attempting to lock identity
* Users in emotional distress
* Overconfident users seeking validation

In all cases, the invariant holds:

> **The system never decides who someone is, what they should become, or what will happen to them.**

---

## 9. Guiding Sentence (Keep This Visible)

> **The system helps users design evidence of capability and possibility — not predict outcomes or assign identity.**

---

## 10. Implementation Reminder

Before touching Phase 6:

* Phase 5.4 must be implemented, tested, and hardened
* Memory must be safe, visible, and revocable
* No applied logic should exist behind feature flags

This document exists so none of these ideas are lost while Phase 5.4 is secured.

