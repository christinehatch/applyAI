# Phase 5.3 — Boundary vs Adapter Responsibility Mapping
## Bounded Analytical Participation

---

## Purpose

This document maps **each Phase 5.3 requirement** to its correct enforcement layer:

- **Boundary-level impossibility**  
  → What must be structurally impossible, regardless of adapter behavior

- **Adapter-level allowance**  
  → What adapters may do *within strict constraints*

This separation ensures Phase 5.3 remains:
- Mechanically bounded
- Non-authoritative
- Immune to UI drift or prompt creep

---

## Guiding Rule

> The **boundary prevents harm**.  
> The **adapter permits constrained expression**.

If a violation would be dangerous, coercive, or irreversible → **boundary**.  
If a violation would be stylistic, linguistic, or contextual → **adapter**.

---

## Test-to-Responsibility Mapping

### 1. Phase 5.3 Not Triggered Without Explicit Request
**Test:** `test_phase5_3_not_triggered_without_explicit_request`

- ✅ Boundary responsibility
- ❌ Adapter must never infer intent

**Boundary must:**
- Require explicit Phase 5.3 trigger phrase or action
- Hard-refuse implicit escalation
- Prevent UI or adapter from activating Phase 5.3 implicitly

---

### 2. Phase Ordering Enforcement
**Test:** `test_phase5_3_requires_prior_phases_completed`

- ✅ Boundary responsibility

**Boundary must:**
- Verify Phase 3 completion
- Reject Phase 5.3 requests out of order
- Prevent adapter invocation entirely if ordering fails

---

### 3. Consent Requirement
**Test:** `test_phase5_3_requires_consent_token`

- ✅ Boundary responsibility

**Boundary must:**
- Require valid consent token
- Enforce revocation immediately
- Make Phase 5.3 impossible without consent

Adapters must never see requests without consent.

---

### 4. Multiple Interpretations Required
**Test:** `test_system_offers_multiple_interpretations_not_single_answer`

- ⚠️ Adapter responsibility
- ✅ Boundary enforces minimum constraints

**Boundary must:**
- Reject adapter output with fewer than 2 interpretations

**Adapter must:**
- Generate plural interpretations
- Never collapse to a single answer

---

### 5. Uncertainty & Optionality Language
**Test:** `test_interpretations_are_clearly_labeled_as_optional`

- ⚠️ Adapter responsibility
- ✅ Boundary enforces forbidden patterns

**Boundary must:**
- Block definitive language patterns

**Adapter must:**
- Use modal language
- Explicitly mark interpretations as optional

---

### 6. User Resonance Selection Required
**Test:** `test_user_must_choose_resonance_or_reject`

- ✅ Boundary responsibility

**Boundary must:**
- Pause progression until explicit user choice
- Prevent adapter continuation without resonance input

Adapters must not assume agreement.

---

### 7. No Recommendations Allowed
**Test:** `test_no_recommendations_are_allowed`

- ✅ Boundary responsibility (hard block)
- ⚠️ Adapter responsibility (avoidance)

**Boundary must:**
- Block recommendation verbs and patterns
- Fail fast on advisory language

---

### 8. No Identity or Trait Labels
**Test:** `test_no_identity_or_trait_labels_are_used`

- ✅ Boundary responsibility

**Boundary must:**
- Reject identity-defining language
- Block trait attribution patterns

Adapters must not attempt soft labeling.

---

### 9. No Clinical or Diagnostic Language
**Test:** `test_no_clinical_or_diagnostic_language`

- ✅ Boundary responsibility

**Boundary must:**
- Block clinical terminology
- Block therapeutic framing
- Block diagnostic inference

---

### 10. Graceful Exit Without Penalty
**Test:** `test_user_can_exit_phase5_3_without_penalty`

- ✅ Boundary responsibility

**Boundary must:**
- Support immediate exit
- Reset Phase 5.3 state
- Prevent adapter re-entry without new explicit request

---

### 11. No Persistence by Default
**Test:** `test_phase5_3_state_is_not_persisted_by_default`

- ✅ Boundary responsibility

**Boundary must:**
- Prevent storage of interpretations
- Prevent memory writes
- Require explicit opt-in for persistence (future Phase 5.4)

---

### 12. No Feedback Into Signal System
**Test:** `test_phase5_3_does_not_modify_signal_counts`

- ✅ Boundary responsibility

**Boundary must:**
- Isolate Phase 5.3 outputs
- Prevent signal mutation
- Prevent detection feedback loops

---

## Responsibility Summary Table

| Concern                              | Boundary | Adapter |
|--------------------------------------|----------|---------|
| Phase triggering                     | ✅       | ❌      |
| Phase ordering                       | ✅       | ❌      |
| Consent enforcement                  | ✅       | ❌      |
| Interpretation plurality             | ✅ (min) | ✅      |
| Uncertainty framing                  | ✅ (ban) | ✅      |
| Resonance gating                     | ✅       | ❌      |
| Recommendations                      | ✅       | ⚠️      |
| Identity / trait labels              | ✅       | ❌      |
| Clinical language                    | ✅       | ❌      |
| Exit handling                        | ✅       | ❌      |
| Persistence                          | ✅       | ❌      |
| Signal isolation                     | ✅       | ❌      |

---

## Core Insight

Phase 5.3 safety does **not** rely on adapter good behavior.

It is enforced by:
- Structural impossibility (boundary)
- Explicit contracts (adapter)
- Failing tests as guardrails

This is what keeps the system from becoming:
> “Just a little advice, but nicely phrased.”

