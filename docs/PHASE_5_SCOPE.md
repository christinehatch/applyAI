# Phase 5 — Learning With Guardrails

Phase 5 marks the transition from **theoretical safety** to **real-world validation**.

After establishing reflection mechanics (Phase 3) and policy boundaries (Phase 4), this phase asks a single question:

> **Can this system safely learn from real user interaction without crossing into inference, authority, or identity formation?**

Phase 5 introduces controlled intelligence under strict constraints.
It prioritizes **trust, consent, and reversibility** over capability expansion.

---

## Core Objective

Phase 5 exists to **validate reflective AI behavior with real users** while preserving:

* User agency
* Psychological safety
* Policy alignment
* Reversibility of interpretation

No new feature is permitted unless it clearly supports this objective.

---

## What Phase 5 Includes

### 1. Controlled AI (LLM) Integration

This is the first phase where a language model may be introduced.

**Allowed uses:**

* Rephrasing *pre-written, vetted* reflection language
* Generating clarifying questions (not insights)
* Summarizing user-provided text **without interpretation**
* Assisting developers in drafting reflection variants (developer-facing only)

**Explicitly disallowed:**

* Novel reflections shown directly to users
* Trait inference or user classification
* Career, aptitude, or identity conclusions
* Cross-session memory or persistence

In Phase 5, the LLM acts as a **language assistant**, not a reasoning authority.

---

### 2. Prompt Expansion (Breadth Over Depth)

Phase 5 may expand prompt variety to:

* Test signal robustness
* Observe pattern emergence across domains
* Identify ambiguity or failure modes

**Constraints:**

* Conversations remain short and session-scoped
* No long-form emotional or therapeutic dialogue
* No deep personalization

The goal is **pattern validation**, not intimacy.

---

### 3. Signal Validation & Calibration

Phase 5 explicitly evaluates whether:

* Signals appear reliably in real use
* Reflection language feels accurate and respectful
* Disagreement feels safe and normal
* Signals overlap or conflict in practice

This learning is **developer-facing only**.
Users are never shown signal names, counts, or diagnostics.

---

### 4. Consent & Control UX

Phase 5 introduces explicit consent moments, including:

* Opt-in to reflections
* Opt-in to follow-up questions
* Clear session endings
* Explicit opt-out paths

Consent must be:

* Clear
* Revocable
* Non-coercive
* Understandable without technical context

The system must function fully even if the user declines reflection.

---

### 5. Session Closure & Safety Guarantees

Every session must include:

* Clear closure language
* Explicit time-scoping (“this conversation only”)
* No implication of assessment or evaluation

Users should never leave feeling:

* Judged
* Categorized
* Analyzed
* Reduced to a pattern

---

## What Phase 5 Explicitly Excludes

The following are **out of scope** for Phase 5:

* Job or role recommendations
* Project suggestions tied to employability
* Resume framing or optimization
* Longitudinal user memory
* Personality typing
* Population comparisons
* Predictive success claims
* Automated advice or guidance

These may only be considered in later phases under new policy review.

---

## Success Criteria

Phase 5 is successful if:

* Users feel *seen but not defined*
* Disagreement with reflections feels safe
* AI involvement feels helpful but non-authoritative
* No Phase 4 policy boundary is violated

Phase 5 is **not** measured by:

* Engagement metrics
* Retention
* Perceived intelligence
* Outcome optimization

---

## Guiding Principle

> **If a feature increases intelligence but reduces trust, it does not belong in Phase 5.**

Phase 5 prioritizes learning *how* to build reflective AI safely — not building more of it.

---

## Phase Alignment

* **Phase 3** — Reflection without interpretation
* **Phase 4** — Policy before capability
* **Phase 5** — Learning with guardrails
* **Phase 6+** — Deferred, undefined, and intentionally constrained
