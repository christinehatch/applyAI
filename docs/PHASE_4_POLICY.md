# Phase 4 — Policy Before Capability

Phase 4 defines the **ethical, experiential, and architectural boundaries** for how this system may reason about user thinking patterns *before* introducing new capabilities.

This phase exists to ensure that increased intelligence never outpaces user trust, agency, or clarity.

---

## Core Principle

**The system observes patterns — it does not define people.**

All insights are offered as *optional mirrors*, never as conclusions, predictions, or prescriptions.

---

## What This System Is (and Is Not)

### This system **IS**:

* A reflective tool for noticing *how* a user approaches open-ended problems
* A conversational partner that asks clarifying, perspective-expanding questions
* A pattern-aware system that operates at the level of process, not identity

### This system **IS NOT**:

* A diagnostic tool
* A personality profiler
* A career recommendation engine
* An authority on who a user is or what they should do

---

## Reflection Generation Policy

### Allowed

* Reflection language must be **vetted, pre-written, and human-authored**
* AI may *select* or *rephrase* vetted reflections
* All reflection language must follow the Phase 3 Tone Guard:

  * Observational
  * Tentative
  * Time-scoped
  * Reversible

### Not Allowed

* AI-generated conclusions about the user
* Novel reflective claims not reviewed in advance
* Statements that imply stable traits, abilities, or limitations

---

## Question vs. Insight Policy

### Primary Role: Question-Asking

The system’s default mode is to:

* Ask clarifying questions
* Surface alternative perspectives
* Invite deeper reflection

### Secondary Role: Perspective Prompts (Optional)

The system may suggest *ways of looking* at a problem, framed as invitations:

> “Some people find it useful to think about this in terms of systems or constraints — would you like to explore that?”

The system must **never** assert:

* What the user is really thinking
* What the problem truly is
* What the correct perspective should be

---

## Pattern-to-Context Mapping Policy

The system may describe **contexts or environments** where certain thinking patterns are commonly useful.

### Allowed

* Pattern → environment descriptions
* Neutral, informational framing
* Multiple environments presented simultaneously

Example:

> “People who tend to explore before acting and think in systems often find environments like research, product discovery, or strategy work supportive of that approach.”

### Not Allowed

* Job or role recommendations
* Predictive claims (“you would be good at…”)
* Ranking or narrowing options
* Framing that implies obligation or destiny

---

## Consent Boundaries

### Explicit User Consent Required For:

* Any cross-session or longitudinal pattern tracking
* Any comparison to other users or populations
* Any use of patterns beyond reflective summaries

Consent must be:

* Clear
* Revocable
* Non-coercive
* Understandable without technical knowledge

---

## Reversibility Guarantee

All reflections must be:

* Optional
* Non-binding
* Easy to disagree with
* Non-persistent unless explicitly accepted by the user

The system must treat disagreement as **valid signal**, not error.

---

## Session Scope Policy

### Default Mode

* Session-only interpretation
* No memory of patterns across sessions
* No accumulation of user identity

### Future Longitudinal Mode (Not Yet Implemented)

May only exist if:

* Explicitly enabled by the user
* Transparently explained
* Clearly beneficial to the user
* Never used to constrain or narrow opportunities

---

## Prohibited Inferences

The system must never:

* Infer mental health conditions
* Apply clinical or diagnostic labels
* Compare users to named groups (e.g., ADHD, autism)
* Use stereotypes or population-level assumptions
* Present internal signals as facts about the user

---

## Design Philosophy

This system prioritizes:

* User agency over system confidence
* Reflection over recommendation
* Curiosity over certainty
* Trust over persuasion

If a feature increases capability but reduces agency, it must not be built.

---


## Future Capability Boundary: Project & Resume-Oriented Outputs

Phase 4 does **not** define how AI-generated or AI-suggested projects will work.

However, this phase establishes **binding constraints** that must apply to any future project-related or resume-oriented capabilities.

---

### Explicitly Prohibited (Unless Revisited by Policy)

The system must not, by default:

* Automatically generate resume-ready projects
* Optimize projects primarily for marketability, keywords, or hiring signals
* Frame projects as prescriptions (e.g. “you should build…”)
* Produce artifacts that imply evaluation of employability, readiness, or fit

---

### Required Safeguards (For Any Future Phase)

Any project-related capability must:

* Be **explicitly opt-in**
* Be framed as **exploratory or illustrative by default**
* Preserve **user authorship, intent, and direction**
* Avoid narrowing identity or career trajectory
* Clearly distinguish **learning projects** from **portfolio or resume claims**

---

### Governing Principle

If project generation is introduced, it must follow the same principles as reflective summaries:

* **Optional**
* **Reversible**
* **Non-authoritative**

The system may support exploration, but it must never define what the user *should* build or *should* be.

---

### Deferred Design

The detailed design of project generation, project scaffolding, or resume translation capabilities is **intentionally deferred** to a later phase.

No implementation of these capabilities should proceed without a dedicated policy review.

---

## Phase Alignment

* **Phase 3** established reflective synthesis without interpretation
* **Phase 4** establishes boundaries for future intelligence
* **Phase 5+** may explore adaptive guidance *only within these constraints*

This policy is a living document and must be revisited before any major capability expansion.

