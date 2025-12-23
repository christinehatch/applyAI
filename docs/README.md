# applyAI (MVP)

This document serves as the **navigation hub for applyAI’s design phases**,
linking to detailed documentation for each stage of the project.

applyAI explores how AI can support **self-understanding before career decisions** — by reflecting *how people think*, not telling them who they are.

Instead of starting with resumes, titles, or optimization, applyAI begins with:
- conversation
- reflection
- user validation

This repository contains an early MVP focused on **cognitive exploration and reflective summaries**.

---

## Why This Project Exists

Many people struggle *before* job applications:
- They don’t know how to describe how they think
- They feel misaligned with roles that “should” fit
- They receive advice that doesn’t match their process

applyAI experiments with a different approach:
- observe how people approach open-ended problems
- reflect patterns back carefully
- let users agree, disagree, or ignore those reflections

The goal is **alignment, not labeling**.

---

## What This MVP Demonstrates

- A multi-stage conversational flow (Flask)
- Rule-based signal detection (no ML)
- Adaptive follow-up questions
- Reflective summaries shaped by patterns
- Explicit user validation of reflections

No databases.  
No persistence.  
No recommendations.  
By design.

---

## Project Phases

- **Phase 1** — Cognitive exploration MVP  
- **Phase 2** — Adaptive reflection (rule-based)
- **Phase 3** — Reflective pattern synthesis *(completed)*
- **Phase 4** — Policy before capability *(current)*
- **Phase 5** — Guarded learning & AI integration *(defined, not yet implemented)*

Detailed documentation:
- [`PHASE_3_REFLECTIVE_SYNTHESIS.md`] (docs/PHASE_3_REFLECTIVE_SYNTHESIS.md)
- [`PHASE_4_POLICY.md`](docs/PHASE_4_POLICY.md)
- [`PHASE_4_CAPABILITIES.md`](docs/PHASE_4_CAPABILITIES.md)

---

## Tech Stack

- Python
- Flask
- Jinja templates

---

## Run Locally

```bash
python app.py


Then open:
http://127.0.0.1:5000


## Phase 4 — Policy Before Capability (Current)

Phase 4 focuses on establishing ethical, experiential, and architectural
boundaries before introducing more advanced AI behavior.

Rather than adding intelligence immediately, this phase defines:
- consent requirements
- reversibility guarantees
- limits on inference and recommendation
- allowed UX patterns for future expansion

See:
- PHASE_4_POLICY.md
- PHASE_4_CAPABILITIES.md
