# Phase 5 — LLM Boundary Interface

**(Assisted Sensemaking / Learning With Guardrails)**

This document defines the **technical and behavioral boundaries** for introducing an LLM into applyAI.

The purpose of this phase is not to make the system “smarter,” but to make it **capable of reasoning without becoming authoritative**.

> **The LLM is a contributor, not a decider.**

---

## Core Principle

**The system observes patterns; the LLM explores possibilities.
Neither defines the user.**

All LLM participation must preserve:

* User agency
* Reversibility
* Consent
* Non-authoritative reflection

---

## Architectural Boundary

The LLM is never a first-class speaker.

All interaction flows through app-controlled logic.

```
User ↔ App Logic (Policy + State) ↔ LLM
```

The LLM:

* Cannot see raw system intent
* Cannot control flow
* Cannot decide what is shown
* Cannot persist memory

---

## Layered Boundary Model

### Layer 1 — App-Controlled Frame (Hard Boundary)

The application strictly controls:

* When the LLM is invoked
* Which phase is active
* What consent has been granted
* What task type is allowed
* What tone and framing must be used

The LLM **never**:

* Initiates interaction
* Escalates scope
* Interprets consent
* Determines correctness

This layer is **non-negotiable**.

---

### Layer 2 — Allowed LLM Capabilities (Soft Boundary)

When explicitly enabled, the LLM may:

* Generate **tentative hypotheses**
* Rephrase observed patterns using alternative language
* Surface **multiple interpretations at once**
* Ask reflective or clarifying questions
* Suggest *ways of thinking*, not conclusions

All outputs must:

* Use tentative language
* Present more than one possible lens
* Invite user response or rejection

Example (allowed):

> “One way to look at this might be…
> Another possible interpretation could be…
> If neither fits, we can ignore both.”

---

### Explicitly Forbidden Outputs

The LLM must never:

* Assign traits or identities
  ❌ “You are analytical”

* Predict success or fit
  ❌ “You’d be good at this role”

* Apply diagnostic or clinical labels
  ❌ “This sounds like ADHD”

* Rank interpretations as correct
  ❌ “The most likely explanation is…”

* Assert conclusions
  ❌ “This means you struggle with…”

These are **hard failures**, not stylistic errors.

---

## Output Contract (Structural Boundary)

All LLM responses must conform to a **structured output contract**.

Conceptual example:

```json
{
  "type": "hypothesis | reflection | question",
  "confidence": "exploratory",
  "content": "...",
  "requires_user_validation": true
}
```

This ensures:

* No output is final by default
* The UI can present content appropriately
* User validation is always expected

Free-form, unstructured output is not permitted.

---

## Consent-Gated Invocation

Before invoking Phase 5 LLM behavior, the system must confirm:

* Explicit Phase 5 consent
* Session-only scope (default)
* Exploratory mode enabled

If **any condition is false**, the system falls back to:

* Phase 3 behavior only
* Vetted reflection snippets
* No novel LLM reasoning

---

## Reversion & Shutdown Guarantee

At any point, the user may disengage:

> “Turn this off.”

System behavior must be immediate and silent:

* LLM generation stops
* System reverts to non-generative reflection
* No persuasion or explanation required
* No penalty or loss of function

This must be implemented as a **single-step reversion**.

---

## Long-Term Flexibility Guarantee

This boundary is designed to ensure:

* The LLM can become *more capable over time*
* Without rewriting trust assumptions
* Without invalidating early users
* Without retroactive policy debt

The intelligence may evolve —
the **rules of engagement do not**.

---

## Summary

Phase 5 introduces reasoning **without authority**.

The LLM may:

* Explore
* Suggest
* Question
* Reframe

It may never:

* Decide
* Diagnose
* Predict
* Define

If a future capability violates this boundary, it does not belong in applyAI.

---

*This document must be reviewed before any expansion of LLM reasoning, persistence, or autonomy.*

