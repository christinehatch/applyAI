# Phase 5 — Explicit Consent Framework

## Purpose

Phase 5 introduces **AI-generated reasoning and synthesis**.  
Before any such capability is enabled, the system must obtain **explicit, informed user consent**.

Consent is not a checkbox — it is a *clear understanding of what changes*.

---

## When Consent Is Required

Consent is required **before** the system may:

- Generate novel insights (not just select or rephrase vetted reflections)
- Reason across multiple user responses
- Propose hypotheses about thinking patterns
- Map patterns to environments, roles, or contexts
- Retain or compare patterns beyond a single session

Without consent, the system remains in **Phase 3 behavior**.

---

## Consent Prompt (Primary)

This prompt must appear **before Phase 5 capabilities activate**:

> **“Would you like me to start offering AI-generated reflections and reasoning about how you think?”**

Immediately followed by:

> **“This would mean I may suggest interpretations or patterns that go beyond pre-written reflections.  
> You can disagree with or ignore anything I say, and nothing is saved unless you ask.”**

### Response Options

- **Yes — try this**
- **Not right now**
- **Tell me more first**

Default state is **off**.

---

## Required Disclosures (Plain Language)

Before the user can consent, the system must clearly explain:

### What Changes

- The system may generate *new* reflective language
- The system may notice broader patterns across the conversation
- The system may suggest perspectives, not just ask questions

### What Does NOT Change

- The system does not diagnose
- The system does not assign traits or labels
- The system does not decide what the user is good at
- The system does not store information across sessions (unless explicitly enabled later)

---

## Reversibility Guarantee

At any time, the user must be able to say:

> “Turn this off.”

The system must then:

- Immediately revert to Phase 3 behavior
- Acknowledge the change without argument or persuasion
- Not treat reversal as error or failure

Example system response:

> “Got it — I’ll switch back to reflection-only mode.”

---

## Disagreement Handling

If the user disagrees with an AI-generated insight:

- Disagreement is treated as **valid signal**
- The system must not defend or reinforce the claim
- The system may ask:
  > “Want to say more about what didn’t fit?”
- The system must not attempt to convince or persuade

---

## Consent Scope Levels (Future-Ready)

Phase 5 introduces **session-only consent** by default.

Future phases may introduce additional scopes, each requiring separate consent:

- **This session only** (default)
- **Across multiple sessions**
- **Pattern comparison over time**

No scope escalation is permitted without a new consent prompt.

---

## UX Principles

Consent language must be:

- Understandable without technical knowledge
- Non-coercive
- Easy to decline
- Easy to reverse

If consent feels *pressured*, the design is wrong.

---

## Governing Rule

> **If the user does not clearly understand what the system is about to do, consent has not been given.**

