# Phase 5.4 — Longitudinal Awareness Checklist

> This checklist defines the full scope and completion criteria for Phase 5.4.
> Anything not explicitly listed here is **out of scope** and must not be implemented
> until Phase 5.4 is complete and hardened.

---

## Phase 5.4 Core Question

> **Can insight persist without identity being imposed?**

If any item below is unchecked, Phase 5.4 is not complete.

---

## 1. Entry & Gating

- [ ] Phase 5.4 is **opt-in only**
- [ ] Consent is **separate** from Phase 5.3 (no shared token)
- [ ] Phase ordering enforced (only after Phase 3 / Phase 5.3 loops complete)
- [ ] No memory logic reachable without explicit user action
- [ ] No automatic upgrades into memory mode

**Fail condition:** memory happens implicitly or by default.

---

## 2. Memory Proposal Rules

- [ ] Memory is **proposed**, never written automatically
- [ ] Proposal occurs immediately after a concrete artifact:
  - [ ] Phase 3 reflection, or
  - [ ] Phase 5.3 interpretation + resonance choice
- [ ] Each memory item is shown **verbatim** before approval
- [ ] User can **edit**, **approve**, or **decline** each item
- [ ] Declining has **no side effects**

**Fail condition:** the system stores something the user never saw or approved.

---

## 3. Memory Content Constraints (Critical)

- [ ] Memory phrasing is **non-identity-locking**
  - Allowed: “has found it useful to…”
  - Disallowed: “is the kind of person who…”
- [ ] No clinical or diagnostic language
- [ ] No inferred traits
- [ ] No hidden scores, signals, or classifications
- [ ] Memory represents **user-endorsed material**, not system conclusions

**Fail condition:** memory reads like a personality label.

---

## 4. Memory Ledger (User Visibility)

- [ ] User can view **all stored memory items**
- [ ] Each item displays:
  - [ ] Exact wording
  - [ ] Timestamp
  - [ ] Source (reflection / interpretation)
- [ ] User can delete any item at any time
- [ ] Deletion is immediate and final from the user’s perspective

**Fail condition:** opaque or “ghost” memory.

---

## 5. Forgetting Guarantees

- [ ] Forget action removes item from:
  - [ ] Memory ledger
  - [ ] Retrieval index
  - [ ] Any future prompt context
- [ ] Forgotten items are never reintroduced
- [ ] System does not argue against forgetting

**Fail condition:** system recalls deleted information.

---

## 6. Retrieval & Use Constraints

- [ ] Memory is **never auto-consumed**
- [ ] Memory is only used when the user explicitly selects it
- [ ] Any memory usage is attributed:
  - “Using the items you selected…”
- [ ] Memory does **not** affect:
  - [ ] signal detection
  - [ ] interpretation thresholds
  - [ ] reflection phrasing
  - [ ] follow-up question logic

**Fail condition:** memory subtly alters behavior without user action.

---

## 7. No Application Leakage (Hard Boundary)

- [ ] No project suggestions
- [ ] No job roles
- [ ] No career framing
- [ ] No planning or optimization language
- [ ] No “next steps” beyond memory management

**Fail condition:** anything that resembles Phase 6 functionality.

---

## 8. Emotional & Epistemic Safety

- [ ] System reinforces that memory is optional
- [ ] System reinforces that memory ≠ identity
- [ ] User disagreement is always valid
- [ ] No pressure to persist insight

**Fail condition:** memory feels like a commitment or definition.

---

## 9. Test Coverage

- [ ] Tests for:
  - [ ] consent gating
  - [ ] proposal-before-write
  - [ ] identity-locking phrase rejection
  - [ ] deletion guarantees
- [ ] Tests pass with memory enabled and disabled
- [ ] Phase 5.3 tests remain unchanged and passing

**Fail condition:** Phase 5.4 breaks Phase 5.3 guarantees.

---

## 10. Final Phase 5.4 Invariant

If this sentence is ever false, Phase 5.4 is broken:

> **“The system can remember what the user approved, without deciding who the user is.”**

---

## Implementation Reminder

Before touching Phase 6:

- Phase 5.4 must be fully implemented, tested, and hardened
- Memory must be safe, visible, and revocable
- No applied or career logic should exist behind feature flags

This checklist exists to prevent accidental scope creep while building Phase 5.4.

