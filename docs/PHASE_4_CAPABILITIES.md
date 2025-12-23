# Phase 4 — Capability Sketches (UX)

Phase 4 introduces **new conversational capabilities** while strictly honoring the Phase 4 policy:
*policy before capability, reflection before inference, agency before automation.*

These sketches describe **what the user experiences**, not how it is implemented.

---

## Capability 4.1 — Reflection Clarification Prompt

### Trigger

After a reflective summary is shown, the user is asked:

> “Does this feel accurate based on how you think and work?”

### User Actions

* **Yes**
* **Somewhat**
* **No**
* Optional free-text response

### System Behavior

* Agreement strengthens confidence in *reflection framing*, not conclusions
* Disagreement is treated as valid signal, not error
* No reflection is “locked in” without user acceptance

### UX Goal

Reinforce that:

* Reflections are optional
* User judgment supersedes system interpretation
* Disagreement is safe and expected

---

## Capability 4.2 — Perspective Expansion (When User Is Stuck)

### Trigger

User expresses uncertainty, confusion, or requests help:

> “I don’t know what to do next”
> “I’m not sure how to think about this”

### System Response (Example)

> “Some people find it useful to think about this in terms of constraints or systems.
> Others start by exploring examples or edge cases.
> Would either of those be helpful to try?”

### Constraints

* Presents **multiple perspectives at once**
* Uses *invitational language*
* Never asserts which is “better”

### UX Goal

Help users **move their thinking**, not accept the system’s thinking.

---

## Capability 4.3 — Pattern Awareness Recap (End of Session)

### Trigger

Conversation reaches natural conclusion

### System Output (Example)

> “During this conversation, you often explored context before committing to action, and you returned to structure when things felt unclear.”

### Characteristics

* Time-scoped (“during this conversation”)
* Observational, not interpretive
* No signal names, counts, or labels

### UX Goal

Offer a **clean mirror**, not a takeaway judgment.

---

## Capability 4.4 — Pattern-to-Context Mapping (User-Initiated)

### Trigger

User explicitly asks:

> “What kinds of jobs would I be good at?”
> “How does this relate to careers?”

### System Reframe (Always)

> “I can’t tell you what you’d be good at, but I can show where similar thinking patterns are often valued. Would that be useful?”

(Requires confirmation before continuing.)

### System Output (Example)

> “The patterns that appeared here — exploration-first thinking and attention to system relationships — are often useful in environments like:
>
> * research and investigation
> * early product discovery
> * systems or architecture-focused work
> * strategy or planning contexts
>
> This isn’t a recommendation — just a way to notice where similar approaches are commonly supported.”

### UX Goal

Support exploration **without narrowing identity or outcomes**.

---

## Capability 4.5 — Opt-In Longitudinal Awareness (Future)

### Trigger

Only after repeated sessions and explicit user request

### Consent Prompt (Example)

> “Would you like me to notice patterns across multiple conversations?
> This would let reflections build over time, but nothing would be saved without your permission.”

### Rules

* Off by default
* Clear explanation of what changes
* Easy opt-out at any time

### UX Goal

Make persistence a **user choice**, not a system assumption.

---

## Capability 4.6 — Reflection Comparison (Optional, User-Driven)

### Trigger

User asks:

> “Has this changed from last time?”

### System Response

* Only allowed if longitudinal mode is enabled
* Describes *difference in process*, not improvement or regression

Example:

> “Compared to last time, you seemed to move toward structure more quickly when uncertainty appeared.”

### UX Goal

Support self-observation **without evaluation**.

---

## What Phase 4 Deliberately Does Not Include

* Job recommendations
* Personality labels
* Predictive success claims
* Ranking or scoring
* Automated advice
* Hidden profiling
* Population comparisons (e.g. ADHD, Myers-Briggs)

---

## Phase 4 UX Philosophy

If a user leaves feeling:

* Seen but not categorized
* Supported but not directed
* Curious rather than corrected

Then Phase 4 is working.

These capabilities are designed to **expand thinking space**, not collapse it.

