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
