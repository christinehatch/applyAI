# Phase 5.5 — Product Integration

**Phase goal:**  
Integrate Phase 5.4’s ethical memory primitives into a user-facing product **without violating architectural or ethical invariants**.

> Phase 5.5 is about *exposure without interpretation*.

---

## 5.5.0 Scope Definition (Required before coding)

- [ ] Phase 5.4 invariants explicitly restated and unchanged
- [ ] No memory writes without proposal + approval
- [ ] No AI-generated memory without mechanical constraints
- [ ] No auto-recall or auto-use of memory
- [ ] Memory remains optional and non-authoritative

---

## 5.5.1 Consent UI

- [ ] Explicit, time-scoped consent language (no blanket consent)
- [ ] Clear distinction between:
  - reflection
  - analysis
  - memory
- [ ] Visual indicator when memory proposals are generated
- [ ] No dark patterns or implied consent
- [ ] Ability to continue using the system with memory disabled
- [ ] Consent revocation path is clear and immediate

---

## 5.5.2 Memory Ledger UI

- [ ] Read-only list of approved memories
- [ ] Separate list of pending proposals
- [ ] Clear provenance per memory item:
  - source (reflection / user-written / system-generated)
  - created_at timestamp
- [ ] No scores, traits, labels, or categories visible to the user
- [ ] Ledger is inspectable but not interpretive
- [ ] Ledger language is descriptive, not evaluative

---

## 5.5.3 Approve / Decline / Forget Flows

- [ ] Approve is an explicit, per-item action
- [ ] Decline requires no justification
- [ ] Forget removes memory from all future use
- [ ] Forget does NOT retroactively reinterpret past outputs
- [ ] All actions are reversible where logically possible
- [ ] UI copy avoids “learning about you” or “knowing you better” language
- [ ] Declined items do not reappear unless explicitly re-proposed

---

## 5.5.4 Selection → Prompt Attribution

- [ ] Memory is only used when explicitly selected
- [ ] Selected memory is visibly attributed in the prompt
- [ ] Users can remove memory from the prompt before sending
- [ ] No hidden memory injection
- [ ] Prompt construction is inspectable (at least conceptually)
- [ ] System never implies memory was used if it was not

---

## 5.5.5 Hard Boundary Enforcement (Runtime)

- [ ] Memory cannot be used for diagnosis, prediction, or evaluation
- [ ] Memory cannot override or contradict user disagreement
- [ ] Memory cannot escalate tone, authority, or certainty
- [ ] Boundary violations fail closed (memory ignored)
- [ ] Violations are logged internally but not exposed as judgments
- [ ] Boundary enforcement is mechanical, not prompt-only

---

## 5.5.6 Forbidden Inferences (Even With AI)

- [ ] Explicit list of forbidden inferences defined, including:
  - identity
  - personality traits
  - mental health status
  - moral character
- [ ] Forbidden even if:
  - user implies them
  - AI is confident
  - patterns appear consistent
- [ ] Enforced at runtime and/or validation layer
- [ ] Forbidden inferences cannot be written to memory
- [ ] Forbidden inferences cannot appear in summaries

---

## 5.5.7 AI-only Signals vs Human-visible Signals

- [ ] Signals explicitly classified as:
  - AI-only (never shown)
  - Human-visible (reflection-safe)
- [ ] AI-only signals may guide:
  - pacing
  - follow-up questions
- [ ] AI-only signals may NOT:
  - appear in summaries
  - influence memory wording
  - be persisted
- [ ] Classification documented and testable

---

## 5.5.8 Memory Decay & Context Expiration

- [ ] Define whether memories decay, expire, or soften over time
- [ ] Expiration affects:
  - availability
  - salience
  - suggestion (never auto-use)
- [ ] Decay rules are transparent or user-controlled
- [ ] No silent reinterpretation of old memories
- [ ] Expired memories do not resurface without re-approval

---

## 5.5.9 Disagreement as a First-Class Signal

- [ ] Explicit user disagreement is captured
- [ ] Disagreement suppresses future similar reflections
- [ ] Disagreement is not treated as resistance or denial
- [ ] Disagreement never triggers escalation
- [ ] System can say “we’ll drop this” and actually do so
- [ ] Disagreement does not penalize or degrade experience

---

## 5.5.10 What the System Is Never Allowed to Say

- [ ] Banned phrase list defined and enforced, including:
  - “This means you are…”
  - “You tend to be the kind of person who…”
  - “Based on your history…”
- [ ] No authority framing
- [ ] No predictive framing
- [ ] No identity claims
- [ ] Enforced via validation/tests, not memory
- [ ] Violations fail closed

---

## 5.5.11 Exit Criteria for Phase 5.5

- [ ] User can inspect, approve, decline, and forget memories
- [ ] Memory is never used without visibility
- [ ] System remains correct when user disagrees
- [ ] No new ethical surface area introduced silently
- [ ] Phase 5.6 can focus purely on adversarial & safety hardening

---

**Status:** ⬜ Not Started / ⬜ In Progress / ⬜ Complete  
**Owner:**  
**Notes:**  

## 5.5.12 Route Contracts & Immutability

- Existing Phase 1–3 conversation routes are treated as **read-only**
- `/` (conversation flow) behavior unchanged except for:
  - emitting proposals
  - surfacing summaries
- No consent logic added inside conversation handlers
- Memory logic lives **outside** conversational state machines
- Summary generation callable **without user navigation** (test harness safe)

---

## 5.5.13 Proposal Lifecycle Invariants  
*(Validated by Test Agent)*

- Proposal creation does **not** write memory
- Approved proposal creates **exactly one** memory item
- Declined proposal creates **zero** memory items

**Approved proposal:**
- sets `approved_at`
- does **not** mutate `created_at`

**Declined proposal:**
- sets `decision = declined`
- does **not** set `approved_at`

- Approved proposals never reappear in pending lists
- Declined proposals never reappear unless explicitly re-proposed

---

## 5.5.14 Memory Timestamp Invariants

- `created_at` is set **once**, at approval time
- `updated_at` equals `created_at` on initial creation
- Reading memory does **not** update timestamps
- Viewing ledger does **not** mutate memory
- Timestamp invariants enforced via automated test

✔️ Implemented and verified via deterministic test agent

---

## 5.5.15 Deterministic Test Harness (Non-User)

- Test agent can:
  - simulate full conversation
  - force summary generation
  - approve / decline proposals via **real routes**
- Test agent does **not** bypass routes with internal writes
- Test agent asserts **invariants**, not interpretations
- Test artifacts excluded via `.gitignore`
- Test failures are **hard failures**, not warnings

---

## 5.5.16 What Tests Are Explicitly NOT Allowed To Do

- No direct writes to memory storage
- No synthetic memory injection
- No shortcut “accept all” helpers
- No bypassing consent / proposal routes
- No reliance on global mutable state across tests

---

## 5.5.17 Documentation as a First-Class Artifact

- Route contracts documented **before** modification
- Consent UI designed **before** code
- Tests written to protect **ethics**, not just correctness
- Each Phase 5.5 code change maps to:
  - a checklist item
  - a test assertion
  - a documented invariant

---

## 5.5.18 Exit Criteria (Amended)

Phase 5.5 is complete when:

- Memory lifecycle is correct **and provable**
- Approval and decline are symmetric and safe
- No timestamps drift under repeated runs
- Conversation flow remains untouched
- A future contributor can:
  - read the checklist
  - run the test agent
  - understand what must **never** change

