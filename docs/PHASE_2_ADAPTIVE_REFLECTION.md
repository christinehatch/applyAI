# Phase 2 — Adaptive Reflection (Rule-Based)

Phase 2 introduces **lightweight adaptivity** to the conversation —
without introducing interpretation, labeling, or summary-level inference.

This phase focuses on *in-the-moment responsiveness*, not insight.

---

## Core Question

Can a system respond to recurring conversational signals
in a way that feels helpful — without becoming interpretive or intrusive?

---

## What Changes from Phase 1

Phase 2 adds:

- Internal detection of simple cognitive signals
- Session-scoped signal counting
- Carefully phrased follow-up questions
- Escalation based on recurrence, not single events

The core conversation flow remains intact.

---

## Signals (Internal Only)

Signals are:

- Rule-based (keyword matching)
- Session-scoped
- Non-diagnostic
- Never exposed directly to the user

Examples include:
- Support-seeking / uncertainty
- Exploration-first language
- Structure- or systems-oriented phrasing

---

## How Adaptivity Works

When a signal is detected:

1. The system may ask **at most one follow-up**
2. The follow-up is reflective, not corrective
3. Escalation only occurs if the signal recurs
4. The conversation then resumes its normal flow

Example escalation:
- First occurrence: gentle clarification
- Second occurrence: reflective noticing
- No further interruption after escalation

---

## What Phase 2 Still Avoids

Phase 2 explicitly does *not*:

- Shape the final summary
- Aggregate signals across the session
- Infer patterns or tendencies
- Apply labels or scores
- Store data across sessions

Signals exist only to support *immediate reflection*.

---

## Design Principles

- Responsiveness over inference
- Reflection over correction
- Minimal interruption
- User agency preserved at all times

---

## Completion Criteria

Phase 2 is considered complete when the system can:

- Detect recurring signals within a session
- Escalate phrasing based on repetition
- Ask limited reflective follow-ups
- Resume conversation cleanly
- Avoid identity claims or conclusions
- Allow users to validate or reject reflections
