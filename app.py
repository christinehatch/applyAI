# ============================================================
# Signal Visibility Matrix (Phase 3)
# ------------------------------------------------------------
# Purpose:
# Define which cognitive signals influence:
#   - follow-up questions (Phase 2)
#   - summary reflection language (Phase 3)
#   - internal-only control logic
#
# IMPORTANT DESIGN CONSTRAINTS:
# - Signals are NEVER exposed to users as labels
# - No counts, thresholds, or metrics appear in summaries
# - Reflection language is observational, not diagnostic
# - Users may agree, disagree, or ignore reflections
#
# ------------------------------------------------------------
# Signal: support_seeking
# ------------------------------------------------------------
# Detected via:
#   - Keywords (e.g. "help", "mentor", "not sure")
#
# Used for:
#   - Adaptive follow-up questions (Phase 2)
#   - Escalated reflective follow-ups on recurrence
#
# Summary visibility:
#   - INDIRECT only
#   - Enables reflective language about how uncertainty
#     was approached (no mention of "support", counts, or frequency)
#
# Example reflection language:
#   "Moments of uncertainty appeared more than once, and
#    pausing to reflect seemed to help you regain clarity."
#
# ------------------------------------------------------------
# Signal: systems_thinking
# ------------------------------------------------------------
# Detected via:
#   - Structural / relational language
#     (e.g. "system", "flow", "components", "architecture")
#
# Used for:
#   - Internal pattern tracking (Phase 3)
#
# NOT used for:
#   - Adaptive follow-ups (initially)
#
# Summary visibility:
#   - INDIRECT only
#   - Appears as preference for structure or relationships
#
# Example reflection language:
#   "You often oriented yourself by clarifying structure
#    or relationships before moving forward."
#
# ------------------------------------------------------------
# Signal: overwhelmed / avoidance
# ------------------------------------------------------------
# Detected via:
#   - Language indicating shutdown, avoidance, or stuckness
#     (e.g. "too much", "I shut down", "I don't know where to start")
#
# Used for:
#   - Future adaptive reflection (Phase 3+)
#
# Summary visibility:
#   - OPTIONAL
#   - Only if paired with recovery or reflection
#
# Example reflection language:
#   "When things felt abstract or overwhelming, taking
#    a step back seemed to help you re-engage."
#
# ------------------------------------------------------------
# Signal: exploration_first
# ------------------------------------------------------------
# Detected via:
#   - Curiosity, clarification, learning-first language
#
# Used for:
#   - Summary synthesis only
#
# Summary visibility:
#   - INDIRECT
#   - Describes approach, not identity
#
# Example reflection language:
#   "You often explored context and possibilities
#    before committing to action."
#
# ------------------------------------------------------------
# Signals intentionally NOT summary-visible:
# ------------------------------------------------------------
# - execution_bias (early action preference)
# - hesitation markers without reflection
#
# These signals may guide future UX decisions
# but are not surfaced to users in Phase 3.
#
# ------------------------------------------------------------
# Guiding Principle:
# Signals inform reflection language —
# they never become conclusions.
# ============================================================

# ============================================================
# Reflection Tone Guard (Phase 3)
# ------------------------------------------------------------
# Purpose:
# Ensure all user-facing summaries remain reflective,
# non-authoritative, and non-diagnostic.
#
# This system NEVER tells users who they are.
# It offers mirrors, not conclusions.
#
# ------------------------------------------------------------
# Language Rules (Must Always Hold):
#
# ❌ Do NOT use:
#   - Personality labels ("you are a systems thinker")
#   - Absolute claims ("you always", "you never")
#   - Metrics or counts ("multiple times", "three times")
#   - Diagnostic or clinical terms
#   - Authority framing ("the system determined", "this means")
#
# ✅ Use:
#   - Observational phrasing ("appeared", "seemed to")
#   - Tentative language ("may", "often", "tended to")
#   - Time-scoped framing ("during the conversation")
#   - Process-focused descriptions (how, not what)
#
# ------------------------------------------------------------
# Reflection Principles:
#
# 1. Signals inform wording, not conclusions
#    - Internal signal logic is never exposed directly
#
# 2. Reflection is optional and reversible
#    - Users can agree, partially agree, or disagree
#
# 3. Recurrence is implied, never quantified
#    - Use phrases like "more than once" or
#      "at several points", never numbers
#
# 4. No advice yet
#    - Phase 3 reflects patterns
#    - Phase 4 may explore implications
#
# ------------------------------------------------------------
# Quick Self-Check Before Adding Any Summary Sentence:
#
# - Could a user reasonably say "That doesn't feel right"?
#   → If not, rewrite.
#
# - Does this sentence name a trait or identity?
#   → If yes, remove or soften.
#
# - Does this sound like an observer or an evaluator?
#   → Observer is correct.
#
# ------------------------------------------------------------
# Guiding Question:
# "Does this sentence help the user notice something,
#  without telling them what to conclude?"
# ============================================================

from flask import Flask, render_template, request,  make_response, redirect, url_for
from signals import (
    SUPPORT_SIGNAL,
    detect_support_signal,
    detect_systems_signal,
    detect_exploration_signal
)
from pathlib import Path
import os
from telemetry import EventLogger

from reflections import (
    collect_reflections,
    generate_base_summary
)
from phase5.request import LLMRequest
from phase5.roles import ParticipantRole, IntelligenceMode
from phase5.boundary import LLMBoundary
from phase5.memory import (
    MemoryItem,
    MemoryKind,
    MemoryNotFoundError,
    MemorySelectionContextBuilder,
    MemorySource,
    MemoryValidationError,
    validate_memory_text,
)
from phase5.consent import get_consent_state, ConsentState
from datetime import datetime, timezone
from memory.file_store import FileBackedMemoryStore
from memory.storage import append_proposal
from phase6.handoff import (
    HandoffTooLargeError,
    HandoffValidationError,
    PendingHandoffStore,
    parse_envelope,
)
import threading
import time
import uuid

app = Flask(__name__, template_folder="templates")

OWNER_COOKIE_NAME = "ce_owner_id"
OWNER_COOKIE_MAX_AGE = 60 * 60 * 24 * 365 * 2  # 2 years (dev-friendly)

def get_or_create_owner_id():
    owner_id = request.cookies.get(OWNER_COOKIE_NAME)
    if owner_id:
        return owner_id, False
    return str(uuid.uuid4()), True

def attach_owner_cookie(resp, owner_id: str, created: bool):
    if created:
        resp.set_cookie(
            OWNER_COOKIE_NAME,
            owner_id,
            max_age=OWNER_COOKIE_MAX_AGE,
            httponly=True,
            samesite="Lax",
            # secure=True,  # turn on when you’re HTTPS
        )
    return resp

LOG_ENABLED = os.getenv("CAREER_EXPLORER_LOGGING", "0") == "1"

# Create a sticky run id once per terminal/server start.
# The Werkzeug reloader will spawn child processes that inherit this env var.
if LOG_ENABLED and "CAREER_EXPLORER_RUN_ID" not in os.environ:
    os.environ["CAREER_EXPLORER_RUN_ID"] = f"run-{int(time.time())}-{uuid.uuid4().hex[:8]}"

# Werkzeug debug reloader uses two processes. Only the child should log.
RELOADER_ACTIVE = "WERKZEUG_RUN_MAIN" in os.environ
IS_RELOADER_CHILD = os.environ.get("WERKZEUG_RUN_MAIN") == "true"

SHOULD_LOG = LOG_ENABLED and (IS_RELOADER_CHILD or not RELOADER_ACTIVE)

logger = EventLogger(
    enabled=SHOULD_LOG,
    base_dir=Path(__file__).resolve().parent / "logs",
)

llm_boundary = LLMBoundary()

# ------------------------------------------------------------
# Per-owner conversation state
# ------------------------------------------------------------
# Each owner (identified by the ce_owner_id cookie) gets an isolated,
# in-memory conversation. State is never shared between owners and is
# never written to disk. It is lost on process restart, by design.

#
# Consent is opt-in: every conversation (new or reset) starts with no
# Phase 5 consent token. Nothing in this module may grant one implicitly.


def new_conversation_state(owner_id: str) -> dict:
    return {
        "session_id": str(uuid.uuid4()),
        "owner_id": owner_id,
        "stage": 1,
        "responses": {},
        "questions_logged": set(),
        "followup": None,
        "followup_answers": None,
        "conversation_log": [],
        "signal_counts": {
            "support_seeking": 0,
            "overwhelmed": 0,
            "systems_thinking": 0,
            "exploration_first": 0
        },
        "signal_escalated": {
            "support_seeking": False
        },
        "feedback": {
            "rating": "...",
            "detail": "..."
        },
        "phase5_consent_token": None,
        "phase5_offer_shown": False,
        # Phase 5.4 memory. Separate from Phase 5 consent: memory opt-in
        # never grants or reads phase5_consent_token, and vice versa.
        "summary_ready": False,
        "summary_reflections": [],
        "memory_opt_in": False,
        "proposals_emitted": False,
        "selected_memory_ids": [],
        # Phase 6.0: validated role envelope the user accepted, or None.
        # Session-only; never written to disk.
        "role_context": None,
    }


_conversation_states: dict = {}
_conversation_states_lock = threading.Lock()


def get_conversation_state(owner_id: str) -> dict:
    """Return this owner's conversation state, creating it on first use."""
    if not owner_id:
        raise ValueError("owner_id is required for conversation state")
    with _conversation_states_lock:
        state = _conversation_states.get(owner_id)
        if state is None:
            state = new_conversation_state(owner_id)
            _conversation_states[owner_id] = state
        return state


def reset_conversation_state(owner_id: str) -> dict:
    """Replace this owner's conversation with a fresh one. Other owners are untouched."""
    if not owner_id:
        raise ValueError("owner_id is required for conversation state")
    state = new_conversation_state(owner_id)
    with _conversation_states_lock:
        _conversation_states[owner_id] = state
    return state
QUESTIONS = {
    1: (
        "Imagine you’re asked to help design a new app for helping people "
        "navigate a city in a way that feels playful and less stressful.\n\n"
        "What do you think this project is asking for?"
    ),
    2: "How would you actually start working on this?",
    3: "What feels most challenging or uncertain when you think about executing this idea?"
}





MAX_STAGE = max(QUESTIONS.keys()) + 1

# Internal-only interpretation of user feedback
# NEVER shown to users
FEEDBACK_INTERPRETATION = {
    "yes": "aligned",
    "somewhat": "partially_aligned",
    "no": "misaligned"
}


def debug_log(conversation_state, title, data=None):
    print("\n" + "-" * 40)
    print(title)
    if data is not None:
        print(data)
    logger.event(
        session_id=conversation_state.get("session_id", "unknown"),
        event_type=f"debug.{title.lower().replace(' ', '_')}",
        payload=data if isinstance(data, dict) else {"data": data},
    )

def append_to_log(
    conversation_state,
    speaker: str,
    content: str,
    content_type: str,
    phase: int
):
    entry = {
        "id": str(uuid.uuid4()),
        "speaker": speaker,           # "system" | "user" | "ai"
        "content": content,
        "content_type": content_type,
        "phase": phase,
        "timestamp": time.time()
    }

    conversation_state["conversation_log"].append(entry)

    logger.event(
        session_id=conversation_state.get("session_id", "unknown"),
        event_type="conversation.message",
        payload=entry,
    )


def insight_log(event, data=None):
    print("\n🧠 INSIGHT:", event)
    if data:
        for k, v in data.items():
                print(f"  - {k}: {v}")


def looks_like_phase5_request(text: str) -> bool:
    triggers = [
        "analyze",
        "analysis",
        "pattern",
        "what does this say",
        "interpret",
        "reason through",
        "deeper"
    ]
    text_lower = text.lower()
    return any(t in text_lower for t in triggers)

def should_offer_phase5_consent(user_input, state) -> bool:
    if state["phase5_consent_token"] is not None:
        return False
    if state.get("phase5_offer_shown"):
        return False
    if not looks_like_phase5_request(user_input):
        return False
    return True

def should_explain_phase5_limits(user_input, state) -> bool:
    if state["phase5_consent_token"] is not None:
        return False
    if not state.get("phase5_offer_shown"):
        return False
    return looks_like_phase5_request(user_input)


def generate_summary(responses, conversation_state):
    summary = []

    # 1. Base heuristic summary (from reflections module)
    summary.extend(generate_base_summary(responses))

    # 2. Phase 3 reflective snippets
    reflections = collect_reflections(conversation_state)
    summary.extend(reflections)

    # --- Phase 5.4: summary only *records* what could be proposed ---
    # No proposals are written here. The user must opt in explicitly via
    # POST /memory/opt-in, which is only reachable after this point.
    conversation_state["summary_reflections"] = list(reflections)
    conversation_state["summary_ready"] = True
    # --- end Phase 5.4 ---

    debug_log(conversation_state, "SUMMARY FEEDBACK ALIGNMENT", {
        "interpretation": conversation_state["feedback"].get("interpretation"),
        "signals_visible": [
            k for k, v in conversation_state["signal_counts"].items()
            if v > 0
        ]
    })

    return " ".join(summary)

@app.route("/", methods=["GET", "POST"])
def home():
    owner_id, owner_created = get_or_create_owner_id()
    conversation_state = get_conversation_state(owner_id)
    stage = conversation_state["stage"]

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()

        # --- Phase 5 consent interception ---
        if should_offer_phase5_consent(user_input, conversation_state):
            conversation_state["phase5_offer_shown"] = True
            append_to_log(
                conversation_state,
                speaker="system",
                content="AI-assisted reasoning is available with consent.",
                content_type="consent_offer",
                phase=5
            )
            resp = make_response(render_template("phase5_consent.html", prompt_type="offer"))
            return attach_owner_cookie(resp, owner_id, owner_created)

        if should_explain_phase5_limits(user_input, conversation_state):
            append_to_log(
                conversation_state,
                speaker="system",
                content="Reflection-only mode is active. Analysis is disabled.",
                content_type="consent_limits",
                phase=5
            )
            resp = make_response(render_template("phase5_consent.html", prompt_type="limits"))
            return attach_owner_cookie(resp, owner_id, owner_created)
        # --- end Phase 5 interception ---

        _ = llm_boundary.evaluate(
            LLMRequest(
                user_text=user_input,
                role=ParticipantRole.OBSERVER,
                intelligence_mode=IntelligenceMode.NONE,
                consent_token=conversation_state["phase5_consent_token"],
                disallowed_capabilities=["recommendation", "diagnosis"]
            )
        )


        if user_input:
            append_to_log(
                conversation_state,
                speaker="user",
                content=user_input,
                content_type="user_response",
                phase=conversation_state["stage"]
            )

            debug_log(conversation_state, "USER INPUT", {
                "stage": conversation_state["stage"],
                "text": user_input,
                "followup_active": bool(conversation_state["followup"])
            })

            # CASE 1: answering a follow-up
            if conversation_state["followup"]:
                conversation_state["followup_answers"] = user_input
                conversation_state["followup"] = None
                conversation_state["stage"] += 1

                debug_log(conversation_state, "FOLLOW-UP ANSWER STORED", {
                    "answer": user_input,
                    "next_stage": conversation_state["stage"]
                })

            # CASE 2: normal stage response
            else:
                stage = conversation_state["stage"]
                conversation_state["responses"][stage] = user_input

                # Passive detection: systems thinking (summary-only)
                if detect_systems_signal(user_input):
                    conversation_state["signal_counts"]["systems_thinking"] += 1
                # Passive detection: exploration-first (summary-only)
                if detect_exploration_signal(user_input):
                    conversation_state["signal_counts"]["exploration_first"] += 1

                fired, debug_info = detect_support_signal(user_input)

                if fired:
                    conversation_state["signal_counts"]["support_seeking"] += 1
                    count = conversation_state["signal_counts"]["support_seeking"]

                    if count <= len(SUPPORT_SIGNAL["questions"]):
                        # 1️⃣ Assign follow-up
                        conversation_state["followup"] = SUPPORT_SIGNAL["questions"][count - 1]

                        # 2️⃣ Log follow-up ONCE
                        append_to_log(
                            conversation_state,
                            speaker="system",
                            content=conversation_state["followup"],
                            content_type="followup_question",
                            phase=2
                        )

                        # 3️⃣ Lock escalation if needed
                        if count == SUPPORT_SIGNAL["max_escalation"]:
                            conversation_state["signal_escalated"]["support_seeking"] = True

                    else:
                        debug_log(conversation_state, "SUPPORT SIGNAL OBSERVED (NO ESCALATION)", {
                            "count": count,
                            "reason": "already_escalated"
                        })

                    # If the signal fired but we intentionally did not interrupt,
                    # continue normal stage progression
                    if conversation_state["followup"] is None:
                        conversation_state["stage"] += 1

                    debug_log(conversation_state, "SUPPORT SIGNAL FIRED", {
                        "signal": SUPPORT_SIGNAL["id"],
                        "details": debug_info
                    })

                else:
                    conversation_state["stage"] += 1

                    debug_log(conversation_state, "SUPPORT SIGNAL NOT FIRED", {
                        "signal": SUPPORT_SIGNAL["id"],
                        "details": debug_info
                    })
            debug_log(conversation_state, "STATE SUMMARY", {
                "stage": conversation_state["stage"],
                "followup_active": bool(conversation_state["followup"]),
                "support_count": conversation_state["signal_counts"]["support_seeking"],
                "support_escalated": conversation_state["signal_escalated"]["support_seeking"]
            })

            stage = conversation_state["stage"]

    if stage in QUESTIONS:
        # ----- Render state (every request) -----
        question = QUESTIONS[stage]
        alternate_question = None

        # ----- Log question ONCE -----
        if stage not in conversation_state["questions_logged"]:
            append_to_log(
                conversation_state,
                speaker="system",
                content=question,
                content_type="question",
                phase=1
            )
            conversation_state["questions_logged"].add(stage)

        # ----- Phase 5.2 paraphrase (render concern) -----
        if conversation_state["phase5_consent_token"]:
            paraphrase_response = llm_boundary.evaluate(
                LLMRequest(
                    user_text=question,
                    role=ParticipantRole.OBSERVER,
                    intelligence_mode=IntelligenceMode.SHALLOW,
                    consent_token=conversation_state["phase5_consent_token"],
                    disallowed_capabilities=["recommendation", "diagnosis"],
                    content_type="question"
                )
            )

            if paraphrase_response.status == "paraphrased":
                alternate_question = paraphrase_response.content

        resp = make_response(render_template(
            "index.html",
            conversation_log=conversation_state["conversation_log"],
            question=question,
            alternate_question=alternate_question,
            followup=conversation_state["followup"]
        ))
        return attach_owner_cookie(resp, owner_id, owner_created)
    # Otherwise, show summary
    summary = generate_summary(
        conversation_state["responses"],
        conversation_state

    )
    print(conversation_state["conversation_log"])
    debug_log(conversation_state, "SESSION INTERPRETATION", {
        "signal_counts": conversation_state["signal_counts"],
        "escalations": conversation_state["signal_escalated"],
        "user_feedback": conversation_state["feedback"]
    })


    resp = make_response(render_template(
        "summary.html",
        summary=summary,
        memory_offer_available=bool(conversation_state["summary_reflections"])
        and not conversation_state["proposals_emitted"],
        proposals_emitted=conversation_state["proposals_emitted"],
    ))
    return attach_owner_cookie(resp, owner_id, owner_created)
@app.route("/feedback", methods=["POST"])
def feedback():
    owner_id, owner_created = get_or_create_owner_id()
    conversation_state = get_conversation_state(owner_id)

    feedback_value = request.form.get("feedback")
    feedback_detail = request.form.get("feedback_detail")

    interpretation = FEEDBACK_INTERPRETATION.get(
        feedback_value,
        "unknown"
    )

    conversation_state["feedback"] = {
        "rating": feedback_value,
        "detail": feedback_detail,
        "interpretation": interpretation
    }

    logger.event(
        session_id=conversation_state["session_id"],
        event_type="session.feedback_received",
        payload=conversation_state["feedback"],
    )

    logger.write_session_snapshot(
        session_id=conversation_state["session_id"],
        snapshot={
            "conversation_log": conversation_state["conversation_log"],
            "signal_counts": conversation_state["signal_counts"],
            "signal_escalated": conversation_state["signal_escalated"],
            "feedback": conversation_state["feedback"],
        },
    )

    debug_log(conversation_state, "USER FEEDBACK RECEIVED", {
        "rating": feedback_value,
        "interpretation": interpretation,
        "detail": feedback_detail,
        "signal_counts": conversation_state["signal_counts"],
        "signal_escalated": conversation_state["signal_escalated"]
    })

    resp = make_response(render_template("feedback_thanks.html"))
    return attach_owner_cookie(resp, owner_id, owner_created)

@app.route("/memory")
def view_memory():
    owner_id, owner_created = get_or_create_owner_id()

    store = FileBackedMemoryStore()
    memories = store.list(owner_id)

    from memory.storage import load_proposals
    proposals = load_proposals(owner_id)
    pending = [p for p in proposals if p.get("decision") == "pending"]

    resp = make_response(render_template(
        "memory.html",
        memories=memories,
        proposal_count = len(pending),
        owner_id=owner_id,
    ))
    return attach_owner_cookie(resp, owner_id, owner_created)

@app.route("/memory/proposals")
def view_memory_proposals():
    owner_id, owner_created = get_or_create_owner_id()

    from memory.storage import load_proposals
    from phase5.consent import get_consent_state, ConsentState  # READ-ONLY

    # Load proposals (storage-level data)
    proposals = [
        p for p in load_proposals(owner_id)
        if p.get("decision") == "pending"
    ]

    # 🔒 Step 7: read-only annotation for UI
    for p in proposals:
        p["consent_state"] = get_consent_state(p)

    resp = make_response(render_template(
        "memory_proposals.html",
        proposals=proposals,
        owner_id=owner_id,
        ConsentState=ConsentState,  # expose enum to Jinja
    ))

    return attach_owner_cookie(resp, owner_id, owner_created)


@app.route("/memory/proposals/<proposal_id>/approve", methods=["POST"])
def approve_memory_proposal(proposal_id):
    owner_id, owner_created = get_or_create_owner_id()

    from memory.storage import load_proposals, save_proposals
    proposals = load_proposals(owner_id)

    p = next((p for p in proposals if p.get("proposal_id") == proposal_id), None)
    if not p:
        return f"Proposal {proposal_id} not found for this owner", 404

    # Idempotency: only pending proposals can be decided. Replays are no-ops.
    if p.get("decision") != "pending":
        return redirect(url_for("view_memory_proposals"))

    text = (p.get("proposed_text") or "").strip()

    # 🔒 Phase 5.4 invariant enforcement (proposal stays pending on failure)
    try:
        kind = MemoryKind(p.get("kind"))
    except ValueError:
        return "This proposal has an unsupported memory kind and cannot be saved.", 400
    try:
        validate_memory_text(text)
    except MemoryValidationError:
        return "This proposal's wording can't be saved as memory.", 400

    # Server-generated; created_at == updated_at on creation.
    now = datetime.now(timezone.utc)

    FileBackedMemoryStore().create(MemoryItem(
        id=str(uuid.uuid4()),
        owner_id=owner_id,
        text=text,
        kind=kind,
        source=MemorySource(source_type=p.get("source_type") or "legacy"),
        created_at=now,
        updated_at=now,
        status="active",
    ))

    p["decision"] = "approved"
    p["approved_at"] = now.timestamp()

    save_proposals(owner_id, proposals)

    return redirect(url_for("view_memory_proposals"))


@app.route("/memory/proposals/<proposal_id>/decline", methods=["POST"])
def decline_memory_proposal(proposal_id):
    owner_id, owner_created = get_or_create_owner_id()

    from memory.storage import load_proposals, save_proposals
    proposals = load_proposals(owner_id)

    p = next((p for p in proposals if p.get("proposal_id") == proposal_id), None)
    if not p:
        return f"Proposal {proposal_id} not found for this owner", 404

    # Only pending proposals can be decided; never flip an approved one.
    if p.get("decision") != "pending":
        return redirect(url_for("view_memory_proposals"))

    p["decision"] = "declined"
    p["declined_at"] = time.time()
    # Decline must not retain usable text (Phase 5.4 schema, decline-no-side-effects).
    p["proposed_text"] = ""
    p["decline_reason"] = request.form.get("reason")  # optional

    save_proposals(owner_id, proposals)

    return redirect(url_for("view_memory_proposals"))


@app.route("/memory/opt-in", methods=["POST"])
def memory_opt_in():
    """
    Phase 5.4 entry: the user explicitly asks to review this conversation's
    reflections as memory proposals. Only reachable after the summary.
    Creates proposals only; never memory.
    """
    owner_id, owner_created = get_or_create_owner_id()
    conversation_state = get_conversation_state(owner_id)

    # Phase ordering: proposals only after Phase 3 reflection exists.
    if not conversation_state["summary_ready"]:
        return "Memory proposals are only available after the conversation summary.", 409

    # Idempotent: one emission per conversation.
    if not conversation_state["proposals_emitted"]:
        for text in conversation_state["summary_reflections"]:
            append_proposal(
                owner_id=owner_id,
                proposed_text=text,
                kind=MemoryKind.SELF_OBSERVATION.value,
                source_type="phase3_reflection",
            )
        conversation_state["memory_opt_in"] = True
        conversation_state["proposals_emitted"] = True

    resp = make_response(redirect(url_for("view_memory_proposals")))
    return attach_owner_cookie(resp, owner_id, owner_created)


@app.route("/memory/<memory_id>/forget", methods=["POST"])
def forget_memory(memory_id):
    """Soft-delete one approved memory item. Deleted items are never used again."""
    owner_id, owner_created = get_or_create_owner_id()

    try:
        FileBackedMemoryStore().delete(owner_id, memory_id)
    except MemoryNotFoundError:
        return f"Memory {memory_id} not found for this owner", 404

    conversation_state = get_conversation_state(owner_id)
    conversation_state["selected_memory_ids"] = [
        mid for mid in conversation_state["selected_memory_ids"] if mid != memory_id
    ]

    resp = make_response(redirect(url_for("view_memory")))
    return attach_owner_cookie(resp, owner_id, owner_created)


def build_selected_memory_context(owner_id: str, conversation_state: dict):
    """
    The ONLY way memory may reach any downstream use (prompt building,
    Phase 6). Resolves just the user's explicitly selected, still-active
    items for this owner, and carries the attribution line.
    """
    return MemorySelectionContextBuilder(FileBackedMemoryStore()).build(
        owner_id=owner_id,
        selected_memory_ids=conversation_state["selected_memory_ids"],
    )


@app.route("/memory/select", methods=["GET", "POST"])
def select_memory():
    """
    Let the user choose which approved memory items may be used in this
    conversation. Selection is session-only and never written to disk.
    """
    owner_id, owner_created = get_or_create_owner_id()
    conversation_state = get_conversation_state(owner_id)
    store = FileBackedMemoryStore()

    if request.method == "POST":
        active_ids = {item.id for item in store.list(owner_id)}
        requested = request.form.getlist("memory_id")
        # Keep only this owner's active items, in the order given, no duplicates.
        conversation_state["selected_memory_ids"] = list(
            dict.fromkeys(mid for mid in requested if mid in active_ids)
        )
        resp = make_response(redirect(url_for("select_memory")))
        return attach_owner_cookie(resp, owner_id, owner_created)

    context = build_selected_memory_context(owner_id, conversation_state)
    resp = make_response(render_template(
        "memory_select.html",
        memories=store.list(owner_id),
        selected_ids=set(conversation_state["selected_memory_ids"]),
        context=context,
    ))
    return attach_owner_cookie(resp, owner_id, owner_created)


@app.route("/memory/select/clear", methods=["POST"])
def clear_memory_selection():
    owner_id, owner_created = get_or_create_owner_id()
    get_conversation_state(owner_id)["selected_memory_ids"] = []
    resp = make_response(redirect(url_for("select_memory")))
    return attach_owner_cookie(resp, owner_id, owner_created)


# ============================================================
# Phase 6.0 — Applied Exploration (Path A via role handoff)
# ============================================================
# Contracts: docs/phase6_route_contracts.md
# Scope:     docs/PHASE_6_OPENING_DECLARATION.md
#
# Nothing here writes to memory, proposals, or disk. Role content is
# untrusted plain text, rendered autoescaped, and never combined with
# the user's memory.

pending_handoffs = PendingHandoffStore()

HANDOFF_EXPIRED_MESSAGE = "This handoff expired; send it again from letsA(ppl)I."


def _handoff_expired_response():
    return make_response(render_template("explore_expired.html", message=HANDOFF_EXPIRED_MESSAGE), 404)


@app.route("/explore/role", methods=["POST"])
def receive_role_handoff():
    """Cross-site intake. Validates and parks; binds nothing to anyone."""
    try:
        envelope = parse_envelope(request.form.get("envelope"))
    except HandoffTooLargeError as e:
        return str(e), 413, {"Content-Type": "text/plain; charset=utf-8"}
    except HandoffValidationError as e:
        return f"This role couldn't be received: {e}", 400, {"Content-Type": "text/plain; charset=utf-8"}

    token = pending_handoffs.park(envelope)
    logger.event(
        session_id="phase6-handoff",
        event_type="phase6.handoff_received",
        payload={
            "handoff_id": envelope["handoff_id"],
            "received_at": datetime.now(timezone.utc).isoformat(),
        },
    )
    return redirect(url_for("preview_role_handoff", token=token), code=303)


@app.route("/explore/role/<token>")
def preview_role_handoff(token):
    """Read-only preview. Viewing is not consent; nothing is bound."""
    envelope = pending_handoffs.peek(token)
    if envelope is None:
        return _handoff_expired_response()

    owner_id, owner_created = get_or_create_owner_id()
    resp = make_response(render_template("explore_role_preview.html", envelope=envelope, token=token))
    return attach_owner_cookie(resp, owner_id, owner_created)


@app.route("/explore/role/<token>/accept", methods=["POST"])
def accept_role_handoff(token):
    """Explicit confirmation: bind the role to this owner's conversation."""
    envelope = pending_handoffs.take(token)
    if envelope is None:
        return _handoff_expired_response()

    owner_id, owner_created = get_or_create_owner_id()
    get_conversation_state(owner_id)["role_context"] = envelope

    resp = make_response(redirect(url_for("explore"), code=303))
    return attach_owner_cookie(resp, owner_id, owner_created)


@app.route("/explore/role/<token>/discard", methods=["POST"])
def discard_role_handoff(token):
    pending_handoffs.discard(token)
    return redirect(url_for("home"), code=303)


@app.route("/explore")
def explore():
    """Path A walkthrough for the active role. Deterministic; no LLM."""
    owner_id, owner_created = get_or_create_owner_id()
    conversation_state = get_conversation_state(owner_id)
    role_context = conversation_state["role_context"]

    memory_context = build_selected_memory_context(owner_id, conversation_state)

    resp = make_response(render_template(
        "explore.html",
        envelope=role_context,
        memory_context=memory_context,
    ))
    return attach_owner_cookie(resp, owner_id, owner_created)


@app.route("/explore/role/clear", methods=["POST"])
def clear_role_context():
    """Leave Phase 6 mode. Memory, selection, and conversation are untouched."""
    owner_id, owner_created = get_or_create_owner_id()
    get_conversation_state(owner_id)["role_context"] = None
    resp = make_response(redirect(url_for("home"), code=303))
    return attach_owner_cookie(resp, owner_id, owner_created)


@app.route("/reset")
def reset():
    owner_id, owner_created = get_or_create_owner_id()
    reset_conversation_state(owner_id)

    resp = make_response(redirect(url_for("home")))
    return attach_owner_cookie(resp, owner_id, owner_created)

if __name__ == "__main__":
    app.run(debug=True)