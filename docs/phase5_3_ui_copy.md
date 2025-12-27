# Phase 5.3 — UI Copy (Grounded in Guarantees)
## Bounded Analytical Participation

---

## Design Principle

> The UI must describe **what the system will do**,  
> not what it *hopes* to do.

All copy below is constrained by:
- Boundary-enforced impossibilities
- Adapter-level allowances
- Acceptance tests in `test_phase5_3_flow.py`

If a sentence is not mechanically true, it is not used.

---

## 1️⃣ Phase 5.3 Entry Offer (Explicit, Optional)

### Trigger Context
Shown **only** after:
- Phase 3 reflection is complete
- Valid consent token exists
- User explicitly requests interpretation / analysis

### Copy

**Title**
> Optional Interpretation

**Body**
> If you’d like, I can offer a few possible ways to interpret patterns that appeared earlier.  
>  
> These are *not conclusions* or recommendations — just perspectives you can consider or ignore.

**What This Means (Collapsed / Secondary Text)**
> • You’ll see more than one possible interpretation  
> • None are presented as “the correct” one  
> • You decide whether any resonate — or none do

**Primary Action**
> View possible interpretations

**Secondary Action**
> Skip this

---

## 2️⃣ Interpretation Display (Core Phase 5.3 UI)

### Header
> Possible Interpretations (Optional)

### Intro Text
> Based on what was discussed earlier, here are a few **possible** ways someone *might* interpret those patterns.  
>  
> You’re not expected to agree with any of these.

---

### Interpretation Card Template

Each interpretation must include:

**Label**
> One possible perspective

**Content Rules**
- Uses uncertainty language (“might,” “could,” “may”)
- Refers only to observed conversation patterns
- No advice
- No traits
- No diagnoses
- No future claims

**Example Placeholder (Structure, not content)**
> One way to look at this is that moments of uncertainty sometimes coincided with seeking external input — which *might* reflect how you prefer to think things through collaboratively.

---

## 3️⃣ User Resonance Selection (Required)

### Prompt
> How does this perspective land for you?

### Options (Explicit)
- This resonates
- This partly resonates
- This doesn’t resonate

### Copy Note
> You can choose any option — including none — without affecting what happens next.

---

## 4️⃣ Multi-Interpretation Flow

If multiple interpretations are shown:

**Between Cards**
> You may respond differently to each, or skip any you don’t want to engage with.

**Navigation**
- Next interpretation
- Skip interpretation

No default selection.  
No implicit agreement.

---

## 5️⃣ Exit / Decline Path (Always Available)

### Copy
> You can stop viewing interpretations at any time.

**Action**
> Exit interpretation mode

### System Response (Guaranteed)
> Interpretation mode exited.  
> No interpretations were saved.

---

## 6️⃣ Persistence Disclosure (Strict)

### If No Persistence (Default)
> These interpretations are **not stored** or remembered.

### If Persistence Is Ever Offered (Future Phase 5.4 Only)
> Nothing is saved unless you explicitly choose to save it.

*(Note: Persistence controls are not present in Phase 5.3.)*

---

## 7️⃣ Prohibited UI Language (Never Use)

The UI must never include:

❌ “This means that you are…”  
❌ “You tend to…” (without uncertainty framing)  
❌ “You should…”  
❌ “This suggests you ought to…”  
❌ “Based on psychology…”  
❌ “Many people like you…”  
❌ “The AI thinks…”  

If the system cannot say it safely, the UI cannot imply it.

---

## 8️⃣ Tone Requirements

UI tone must be:
- Observational
- Calm
- Non-authoritative
- Non-therapeutic

Avoid:
- Coaching tone
- Diagnostic framing
- Motivational language
- Insight-as-reward framing

---

## 9️⃣ Safety Alignment Checklist

Before shipping any Phase 5.3 UI:

- [ ] UI never implies correctness
- [ ] UI never pressures engagement
- [ ] UI supports exit at all times
- [ ] UI language matches boundary guarantees
- [ ] UI copy passes adversarial reading (“What if I take this literally?”)

---

## Final Guarantee (User-Facing)

> This feature offers perspectives — not answers.  
> You’re always free to disagree, skip, or stop.

That sentence must remain true.

