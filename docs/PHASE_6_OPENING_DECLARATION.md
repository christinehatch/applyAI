# Phase 6 — Opening Declaration

**Status:** Opened 2026-11-17
**Opens:** Phase 6.0 — Applied Exploration, first increment (Path A via role handoff)
**Depends on:**

* `phase-roadmap.md` §3–§7 and §10 (Phase 6 design, memory rule, entry gate)
* `phase5_4_checklist.md` (Phase 5.4 complete)
* `phase5_5_route_contracts.md` (frozen Phase 5 surfaces; global invariants)
* `phase6_route_contracts.md` (routes this phase may add)
* letsA(ppl)I `docs/APPLYAI_HANDOFF_CONTRACT.md` (the only external input)

---

## 0. Why Phase 6 Can Open Now

`phase-roadmap.md` §10 requires, before any Phase 6 work:

| Requirement | Status | Evidence |
|---|---|---|
| Phase 5.4 implemented | ✅ | opt-in, approve/decline, ledger, forget, selection routes in `app.py` |
| Phase 5.4 tested | ✅ | `tests/test_phase5_4_memory.py`, `tests/test_phase5_4_integration.py`, `test_agent*.py` |
| Memory safe, visible, revocable | ✅ | `phase5_4_checklist.md` §1–§9 |
| No applied logic behind feature flags | ✅ | none exists; see §6 below |

One item is intentionally deferred: injecting selected memory into an LLM
prompt (checklist §6, marked ➖). Phase 6.0 does not use an LLM, so it does
not need it.

---

## 1. Core Question

> **Can insight be applied without turning the system into an authority or oracle?**

Phase 6.0 answers a narrow version of it:

> **Can a user look at one real job posting next to their own approved
> materials, and design ways to show capability, without the system ever
> judging the match?**

---

## 2. Scope of Phase 6.0 (This Increment)

### In scope

1. **Role handoff intake** from letsA(ppl)I, per the handoff contract
   (`/explore/role` routes in `phase6_route_contracts.md`).
2. **Role context** held in the owner's conversation state for the session only.
3. **Path A walkthrough** (`GET /explore`), deterministic, no LLM:
   * the role's capabilities and stated requirements in the posting's own words
   * the posting's project opportunities, framed as "one way to show this would be…"
   * an explicit limits statement: no project guarantees any outcome
   * memory items the user selected via `/memory/select`, shown with the
     attribution line, side by side with the role and never merged into it
4. **Leaving the mode**: "Clear role context" and `/reset`.

### Out of scope (needs its own declaration or contract change)

* **Path B — Discovery Entry** (roadmap §4, §5 Path B)
* **Phase 6.1 — Career Formatting Mode** (roadmap §6)
* **Any LLM use in Phase 6**, including generated project ideas or rewording
* **Gap data** of any kind (handoff contract §11.1)
* **Return path** to letsA(ppl)I (handoff contract §11.2)
* **Education / experience intake** (roadmap Path A mentions it; 6.0 uses only the role and selected memory)
* **Writing memory or proposals from Phase 6**: Phase 6.0 writes nothing to
  `memory.json` or `proposals.json`
* **Hosted deployment** (handoff contract §11.3)

---

## 3. Mode Switch

Phase 6 is explicitly mode-switched, opt-in, and non-default (roadmap §3).

* **Entry** is only through a user-confirmed role handoff: the user sends a
  role from letsA(ppl)I *and* confirms it again on applyAI's preview page.
  Phase 6 never starts from the reflective conversation itself.
* **While in mode**, every Phase 6 page shows a persistent banner naming the
  mode, the source posting, and the framing line: *"This describes what one
  job posting says. It says nothing about you."*
* **Exit** is always one click ("Clear role context") and also happens on
  `/reset` and process restart.
* **Phases 1–5 are unaffected.** The conversation, summary, memory ledger,
  and consent flows behave exactly as before, with or without a role loaded.

---

## 4. Phase 6 Invariants

These hold for every Phase 6 route, page, and future increment unless a new
declaration changes them.

1. **No judgement of fit.** No fit, match, alignment, readiness, or gap
   scores; no "you'd be good at", "you're ready", "you're missing".
2. **No identity assignment.** Phase 5 identity-locking, clinical, and
   authoritative phrase blocks apply to all Phase 6 copy.
3. **No outcome claims.** Every Path A view states that no project
   guarantees an outcome, and never claims sufficiency or optimality.
4. **Exploration framing.** Project concepts are "one way to show this",
   never requirements, credentials, or plans.
5. **No ranking.** Capabilities and projects appear in posting order; nothing
   is sorted by relevance to the user.
6. **Selected memory only.** Memory enters Phase 6 only through
   `build_selected_memory_context()`, with its attribution line visible.
7. **Side by side, never merged.** Role content and user memory are rendered
   in separate, labelled areas. No code path combines them into a derived value.
8. **Session-only role context.** Never written to disk; logs hold only
   `handoff_id` and a server-generated `received_at`.
9. **Untrusted input.** Envelope strings are plain text, autoescaped, never
   rendered as HTML or Markdown, and never fed to an LLM in 6.0.

---

## 5. Relationship to Frozen Phase 5 Surfaces

* Phase 6 **adds** routes; it does not change any route in
  `phase5_5_route_contracts.md`.
* Phase 6 **reads** memory only through `build_selected_memory_context()`.
* Phase 6 **adds** one key to the per-owner conversation state:
  `role_context` (default `None`). `/reset` clears it because it creates a
  fresh state.

---

## 6. No Feature Flags

Roadmap §10 forbids applied logic behind feature flags. Therefore:

* Phase 6 code is merged only when it is complete and tested for the
  increment it belongs to.
* Once merged, `/explore/role` and `/explore` exist unconditionally. There is
  no "off" switch in applyAI.
* Whether a user ever reaches them depends on letsA(ppl)I being configured
  with applyAI's address (handoff contract §8). That is destination
  configuration in another system, not a flag around applied logic here.

---

## 7. Exit Criteria for Phase 6.0

Phase 6.0 is complete when:

- [ ] `phase6_route_contracts.md` routes are implemented as written
- [ ] Every route has tests, including the rejection cases in the handoff contract §9
- [ ] Language guard test: Path A pages contain no fit/score/readiness/identity phrases
- [ ] Tests prove Phase 6 writes nothing to memory or proposals
- [ ] Tests prove role context is per owner and cleared by "Clear role context" and `/reset`
- [ ] An end-to-end run sends a real role from letsA(ppl)I and walks it in applyAI
- [ ] `phase-roadmap.md` updated with what Phase 6.0 learned

---

## 8. Guiding Sentence

> **The system helps users design evidence of capability and possibility —
> not predict outcomes or assign identity.**
