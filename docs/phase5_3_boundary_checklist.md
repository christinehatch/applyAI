# Phase 5.3 — LLMBoundary Responsibility Checklist

## Purpose

This document defines **everything the LLMBoundary must guarantee mechanically**
before **Phase 5.3 (Bounded Analytical Participation)** is allowed to run.

If **any requirement below is violated**, Phase 5.3 **must not execute** —
regardless of UI state, adapter behavior, or developer intent.

This checklist is derived directly from the Phase 5.3 acceptance tests and is
considered **authoritative**.

---

## 🔐 Activation & Ordering Guards

### ⬜ Explicit Invocation Required

Phase 5.3 must **never activate implicitly**.

The user must make a **clear, explicit request** for interpretation.
Passive curiosity, emotional language, or ambiguity is insufficient.

**Blocks**
- `test_phase5_3_not_triggered_without_explicit_request`

---

### ⬜ Prior Phase Completion Verified

Phase 5.3 may only run **after Phase 3 reflection is complete**.

It must not be accessible:
- mid-conversation
- during question collection
- before summary reflection exists

**Blocks**
- `test_phase5_3_requires_prior_phases_completed`

---

### ⬜ Consent Token Required

A valid consent token **must be present at execution time**.

Consent must be:
- explicit
- revocable
- checked by the boundary (not cached elsewhere)

**Blocks**
- `test_phase5_3_requires_consent_token`

---

## 🚫 Capability Prohibitions (Hard Safety)

The following capabilities are **absolutely forbidden** in Phase 5.3.
If requested or inferred, the boundary **must refuse execution**.

---

### ⬜ No Recommendations or Advice

The system must not provide:
- next steps
- suggestions
- guidance
- implied actions

**Disallowed capability**
```python
"recommendation"

