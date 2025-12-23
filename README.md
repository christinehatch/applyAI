# applyAI

applyAI is an exploratory project that investigates how AI can be used **before** job applications — to help people understand how they think, work, and approach problems.

Instead of starting with resumes, job titles, or keyword matching, applyAI begins with **conversation, reflection, and feedback**.

This repository contains an MVP conversational web app that surfaces thinking patterns through short, structured prompts and invites users to confirm or challenge the system’s reflections.

---

## What “applyAI” Means

The name **applyAI** is intentionally multi-layered:

**Apply AI to how you think**
Use AI as a reflective tool to notice problem-solving style, uncertainty handling, and support preferences.

**Apply AI while building projects**
Explore AI as a thinking partner — not just a code generator.

**Apply AI to the job search (future phases)**
Eventually support alignment between how people think and the environments or roles that value those approaches.

This MVP focuses on the **first layer**: self-understanding through AI-guided reflection.

---

## Why This Project Exists

Most career tools optimize for outcomes:

* Job titles
* Skills lists
* Keyword matching

But many people struggle *before* that stage:

* They don’t know how to describe how they think
* They’re unsure which environments fit their working style
* They underestimate strengths that don’t show up on resumes

applyAI experiments with a different approach:

* Present open-ended, domain-agnostic prompts
* Observe how users frame and approach problems
* Reflect patterns back using careful, non-diagnostic language
* Let users confirm, refine, or reject those reflections

The goal is **alignment**, not labeling.

---

## What This MVP Demonstrates

This proof of concept is intentionally small and focused.

It demonstrates:

* A state-driven, multi-stage conversational flow (Flask)
* Structured prompts designed to surface thinking patterns
* Lightweight, rule-based signal detection (no ML)
* Adaptive follow-up questions without interpretation
* Reflective summaries that remain optional and reversible
* A user feedback loop to validate or challenge reflections

The emphasis is on **logic, interaction design, and trust**, not scale.

---

## What’s Intentionally Not Included

This is an MVP, not a finished product.

The following are *deliberately excluded*:

* Persistent user profiles
* Cross-session memory
* LLM-driven interpretation or generation
* Personality typing or diagnostics
* Automated advice or job recommendations
* Styling frameworks or frontend complexity

These constraints are intentional and foundational.

---

## Project Structure

* **`app.py`**
  Conversation flow, state handling, and summary synthesis

* **`signals.py`**
  Pure, rule-based signal detection (stateless)

* **`reflections.py`**
  Guarded reflection snippets mapped from internal signal state

* **`docs/`**
  Detailed phase documentation, policies, and UX sketches

See `docs/README.md` for a guided overview of all project phases.

---

## Project Phases

This repository documents a phased approach to building reflective AI systems:

* **Phase 1** — Cognitive Exploration (MVP)
* **Phase 2** — Adaptive Reflection (Rule-Based)
* **Phase 3** — Reflective Pattern Synthesis
* **Phase 4** — Policy Before Capability *(current)*

Later phases may explore richer AI involvement — but only within clearly defined ethical and experiential boundaries.

---

## How to Run Locally

```bash
python app.py
```

Then open:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

No database, no authentication, no external APIs — by design.

---

## Project Philosophy

This project explores how AI can reflect **thinking patterns** without:

* Labeling
* Diagnosing
* Directing
* Predicting outcomes

Before increasing capability, applyAI prioritizes:

* User agency
* Reversibility
* Transparency
* Policy before inference

If a feature increases intelligence but reduces trust, it doesn’t belong here.

---

For deeper design rationale, ethical constraints, and future capability sketches, see the documentation in `docs/`.

---

*applyAI is an experiment in building AI systems that help people understand themselves — without being reduced by them.*

