# Phase 6 Route Contracts

> **Purpose**: Define, before implementation, what each Phase 6 route is
> allowed and not allowed to do.
>
> Phase 6 routes inherit every **Global Phase 5 Invariant** in
> `phase5_5_route_contracts.md` and every invariant in
> `PHASE_6_OPENING_DECLARATION.md` §4. Where they overlap, the stricter rule wins.

Scope: Phase 6.0 (Path A via letsA(ppl)I role handoff). The envelope format
is defined in letsA(ppl)I `docs/APPLYAI_HANDOFF_CONTRACT.md` §3 and is not
repeated here.

---

## Handoff Flow

```
letsA(ppl)I (other origin)          applyAI
──────────────────────────          ───────
form POST ───────────────────►  POST /explore/role
                                  validate → park under token → 303
                               GET  /explore/role/<token>
                                  preview + "Explore this role" button
                       user ──► POST /explore/role/<token>/accept
                                  bind to owner → 303
                               GET  /explore            (Path A view)
                               POST /explore/role/clear (exit mode)
```

Two steps on the applyAI side are deliberate:

* The cross-site POST does not carry the `ce_owner_id` cookie (`SameSite=Lax`),
  so it cannot be bound to an owner directly.
* Any website can submit a form to `/explore/role`. The same-origin
  **accept** step means a role only becomes active after the user confirms it
  inside applyAI. This is the Phase 6 mode switch.

---

## Pending Handoff Store (internal)

* In-process dict: `token → (envelope, created_at)`.
* Token: 32+ bytes from `secrets.token_urlsafe`.
* Expiry: 5 minutes from creation, server clock.
* Single use: a token is deleted on accept, on expiry check, or when replaced.
* Never written to disk. Lost on restart (the user re-sends from letsA(ppl)I).
* Size bound: at most 100 pending tokens; the oldest is evicted first.

---

## Route: `/explore/role` (POST)

**Purpose**:

* Receive a role handoff envelope from letsA(ppl)I

**Allowed**:

* Parse the `envelope` form field as JSON
* Validate per handoff contract §5.2 (version, system, allowlisted keys, limits, https URL)
* Park a valid envelope under a new token
* Log `handoff_id` and server-generated `received_at` only

**Explicitly Forbidden**:

* Binding the role to any owner or conversation
* Reading or setting the owner cookie
* Writing to memory, proposals, or any file
* Logging envelope content

**Responses**:

* Valid: `303` to `GET /explore/role/<token>`
* Invalid: `400` with a plain-text reason; nothing parked
* Oversize (> 64 KB): `413`; nothing parked

---

## Route: `/explore/role/<token>` (GET)

**Purpose**:

* Show the user what was sent and ask whether to explore it

**Allowed**:

* Render the envelope read-only: company, title, link to `job_url`, summary,
  requirements, capabilities, project opportunities, confidence,
  structural notes, and the framing line
* Offer "Explore this role" (POST to accept) and "Not now" (discard)

**Explicitly Forbidden**:

* Binding the role (viewing is not consent)
* Pre-submitting or auto-submitting the accept form
* Consuming the token

**Responses**:

* Unknown or expired token: `404` page, "This handoff expired; send it again from letsA(ppl)I."

---

## Route: `/explore/role/<token>/accept` (POST)

**Purpose**:

* Explicit user confirmation that binds the role to their conversation

**Allowed**:

* Consume the token
* Set `role_context` in the caller's per-owner conversation state
  (replacing any previous role)

**Explicitly Forbidden**:

* Writing to memory or proposals
* Changing selection, consent, or any Phase 5 state
* Accepting a token that is unknown, expired, or already used

**Responses**:

* Success: `303` to `GET /explore`
* Unknown, expired, or used token: `404` with the same message as above

**Invariants**:

* A token binds to at most one owner, exactly once

---

## Route: `/explore/role/<token>/discard` (POST)

**Purpose**:

* "Not now": drop a pending handoff without binding it

**Invariants**:

* Deletes the token; no other state changes; idempotent

---

## Route: `/explore` (GET)

**Purpose**:

* Path A walkthrough for the active role

**Allowed**:

* Render, in separate labelled areas:
  * **Mode banner**: "Exploring a role", source company and title, framing line, "Clear role context"
  * **The role, in the posting's words**: summary, stated requirements with modality, capabilities with quoted evidence
  * **Ways to show it**: each project opportunity introduced as "One way to show this would be…", with its quoted evidence
  * **Limits**: "No project guarantees an interview, an offer, or any outcome."
  * **Your selected materials**: output of `build_selected_memory_context()`, with attribution; link to `/memory/select`
* Render items in envelope order

**Explicitly Forbidden**:

* Any computed relationship between memory and role (scores, overlaps, highlights, ordering by relevance)
* Fit, match, readiness, gap, or identity language
* LLM calls
* Writing to memory, proposals, or disk

**Responses**:

* No active role: page explaining that a role is sent from letsA(ppl)I, with links to `/` and `/memory`

---

## Route: `/explore/role/clear` (POST)

**Purpose**:

* Leave Phase 6 mode

**Allowed**:

* Set the caller's `role_context` to `None`

**Explicitly Forbidden**:

* Clearing memory, proposals, selection, or conversation progress

**Invariants**:

* Idempotent; redirects to `/`

---

## Changes to Existing Routes

* `/reset`: no code change. It already replaces the owner's state, which
  resets `role_context` to `None`. Contract note added in
  `phase5_5_route_contracts.md`.

---

## Non-Routes (Must Never Exist in Phase 6)

* Any endpoint that returns or stores a user↔role comparison
* Bulk or background handoff intake
* Any endpoint that sends data back to letsA(ppl)I or a third party
* Any endpoint that turns role content into a memory proposal
