applyAI (MVP)

applyAI is an exploratory project that investigates how AI can be applied before job applications — to understanding how people think, work, and engage with problems.

Instead of starting with resumes or job titles, applyAI begins with conversation, reflection, and feedback.

This repository contains the first MVP: a conversational web app that surfaces thinking patterns through short, structured prompts and validates them with the user.

What “applyAI” means

The name applyAI is intentionally multi-layered:

Apply AI to how you think
Gain insight into problem-solving style, uncertainty tolerance, and support needs.

Apply AI while building projects
Learn to collaborate with AI as a thinking partner, not just a code generator.

Apply AI to the job search (future phase)
Eventually help people align projects, roles, and applications with how they actually work best.

This MVP focuses on the first layer: self-understanding through AI-guided reflection.

Why this project exists

Most career tools optimize for outcomes:

Job titles

Skills lists

Keyword matching

But many people struggle before that stage:

They don’t know how to describe how they think

They don’t know which roles fit their working style

They underestimate strengths that don’t show up on resumes

applyAI experiments with a different approach:

Present open-ended, domain-agnostic prompts

Observe how the user frames and approaches problems

Reflect a grounded interpretation back to them

Let the user confirm or correct that interpretation

The goal is alignment, not labeling.

What this MVP demonstrates

This proof of concept intentionally stays small and focused.

It demonstrates:

A state-driven, multi-stage conversational flow using Flask

Structured prompts designed to surface thinking patterns

Simple rule-based pattern inference (no ML yet)

A feedback loop where the user validates or refines the summary

Clear separation between conversation, summary, and feedback stages

The emphasis is on logic, interaction design, and clarity, not scale.

Tech stack

Python

Flask

HTML (Jinja templates)

No database, no authentication, no external APIs — by design.

What’s intentionally not included (yet)

This is an MVP, not a finished product. The following are future phases:

Long-form adaptive conversations (10–20 minute sessions)

Persistent user profiles

LLM-driven analysis or prompt generation

Styling or frontend frameworks

Automated job matching or applications

These are consciously excluded to keep the focus on core behavior.

Future directions

Planned directions include:

Adaptive follow-up questions based on engagement and avoidance signals

Mapping thinking patterns across interests (engineering, design, arts, etc.)

AI-guided project ideas tailored to cognitive style

Portfolio and learning-path generation

Eventually: AI-assisted job discovery and application workflows

How to run locally
python app.py


Then open:
http://127.0.0.1:5000

Project status

This repository represents Phase 1: Cognitive Exploration of applyAI.

It is intentionally small, inspectable, and designed to evolve.

---

## Project Status

## Phase 1 MVP — Cognitive Exploration

This repository represents the first phase of applyAI: a minimal, functional prototype designed to explore how conversational prompts and feedback can surface thinking patterns.

The focus is on clarity, intentional constraints, and extensibility — not completeness or scale.

## Phase 2: Adaptive Reflection (Rule-Based)
**Current phase:** 
Phase 2 introduces lightweight adaptivity without introducing interpretation or labeling.

The system:
- Detects recurring cognitive signals using keywords
- Tracks signal frequency within a session
- Uses escalation phrasing to reflect recurrence gently
- Asks at most one follow-up per detection
- Resumes the core conversation flow cleanly

Signals are used only to guide in-the-moment reflection.
They are not surfaced directly in summaries or used to draw conclusions.

This phase focuses on *responsiveness*, not inference.

##Phase 2 — Completion Checklist

Phase 2: Adaptive Reflection (Rule-Based) is considered complete when the system can:

 - Detect recurring cognitive signals using keyword-based rules

 - Track signal frequency within a single session

 - Escalate follow-up phrasing based on repetition (not single events)

  - Ask at most one reflective follow-up per detection

  - Resume the core conversation flow without disruption

  - Avoid labels, diagnoses, or trait attribution

  - Keep signal logic internal (not exposed directly to the user)

  - Allow the user to validate or challenge the system’s reflection

  - Log feedback for later evaluation and refinement
Phase 3: Pattern Synthesis & Summary Evolution

Phase 3 extends applyAI from in-the-moment reflection to gentle pattern synthesis.

In this phase, signals detected during the conversation are no longer used only to guide follow-up questions. Instead, they begin to inform how the final summary is shaped and phrased — without introducing labels, diagnoses, or fixed traits.

The system focuses on reflecting recurring tendencies rather than isolated moments.

What Phase 3 introduces

Phase 3 explores how repeated signals can influence summaries in a careful, non-interpretive way.

This phase adds:

Multiple signal types beyond support-seeking (e.g. exploration-first, systems thinking, overwhelm)

Lightweight aggregation of signal frequency across a session

Summary language that reflects patterns rather than single responses

Clear separation between:

What was observed

What is reflected

What remains open-ended

Signals remain internal to the system and are never exposed as scores, labels, or diagnostics.

Design principles

Phase 3 follows strict constraints:

No personality typing

No ranking or scoring of users

No claims about fixed traits

No prescriptive recommendations

Instead, summaries evolve through phrasing such as:

“Across the conversation, moments of uncertainty invited reflection on how you like to regain clarity.”

The goal is recognition, not classification.

What Phase 3 does not include

To preserve clarity and trust, Phase 3 intentionally excludes:

LLM-based interpretation

Persistent user profiles

Cross-session memory

Career or role recommendations

Automated advice generation

Those concerns are reserved for later phases.

Why Phase 3 matters

Phase 3 is the bridge between:

Reactive systems (responding to what was just said)

Reflective systems (helping users notice how patterns recur)

It prepares the groundwork for future AI-assisted reasoning while keeping the system transparent, inspectable, and human-centered.
#Phase 3: Pattern Synthesis & Reflective Summaries

Phase 3 focuses on synthesizing signals gathered during the conversation into clearer, user-facing reflection — without introducing labeling, diagnosis, or premature conclusions.

In this phase, the system begins to *use signals holistically*, rather than only for moment-to-moment follow-ups.

##Goals

Phase 3 aims to:

- Translate repeated signals into meaningful reflection

- Help users recognize patterns across their responses

- Preserve user agency by avoiding fixed interpretations

- Maintain a non-evaluative, curiosity-driven tone

##What Changes in Phase 3

Unlike Phase 2, where signals only guide *in-the-moment follow-up questions*, Phase 3 introduces *summary-level synthesis.*

The system may:

- Reference recurring themes implicitly (e.g. “uncertainty surfaced multiple times”)

- Acknowledge patterns without naming or scoring them

- Reflect how the user approached problems, not who they are

Signals are still:

- Session-scoped

- Rule-based

- Transparent and inspectable

##Example Summary Additions (Illustrative)

Rather than exposing signal names or counts, summaries may include language like:

- “You often paused to clarify context before moving forward.”

- “Moments of uncertainty invited additional reflection, which helped clarify next steps.”

- “You balanced exploration with a desire for structure when approaching the problem.”

These reflections are *descriptive, not diagnostic.*

##Signals Used

Phase 3 expands beyond a single signal and may incorporate:

- Support-seeking / uncertainty

- Systems-oriented thinking

- Exploration-first approaches

- Overwhelm or friction signals

- Execution-oriented tendencies

Signals are combined only when helpful — absence of a signal is not treated as a deficit.

##What Phase 3 Still Avoids

Phase 3 intentionally does *not* include:

- Personality typing

- Cognitive labels or profiles

- Scoring, ranking, or normalization

- Persistent user storage

- Automated recommendations tied to roles or careers

Those belong in later phases.

##Why This Phase Matters

Phase 3 is the bridge between:

- Reactive adaptivity (Phase 2)

- and meaningful insight (future phases)

It tests whether reflective summaries feel:

- Accurate

- Respectful

- Useful

- Trustworthy

Before any AI-driven inference is introduced.

## Phase 3 — Reflective Signal Synthesis (Implementation)
This project uses lightweight, rule-based **cognitive signals** to observe *how* a user approaches open-ended problems — without labeling, diagnosing, or prescribing behavior.

### What Phase 3 Adds

Phase 3 introduces a **reflection layer** that:

* Tracks recurring conversational signals (e.g. uncertainty, structure-seeking, exploration-first language)
* Uses those signals to unlock **observational reflection snippets**
* Presents reflections as optional mirrors, not conclusions

No signal names, counts, or thresholds are ever shown to the user.

### Design Principles

* **Signals inform language, not identity**
* **Recurrence is implied, never quantified**
* **All reflection language is tentative and reversible**
* **Users can agree, disagree, or ignore reflections**

This phase is intentionally non-advisory.
It focuses on *pattern awareness*, not guidance or correction.

### Architecture Overview

* `signals.py`
  Defines signal metadata and pure detection functions.
  No state mutation or UI logic.

* `reflections.py`
  Maps internal signal states to reflection snippets using guarded conditions.
  Includes optional debug output for development only.

* `app.py`
  Orchestrates conversation flow, signal counting, follow-up prompts, and summary synthesis.

### Phases Completed

* **Phase 3a** — Signal visibility rules and reflection tone guard
* **Phase 3b** — Reflections refactored into a dedicated module with clean boundaries

Later phases may explore adaptive guidance or AI-generated reflection — without rewriting this foundation.
