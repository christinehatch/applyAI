"""
Phase 6.0 — role handoff intake from letsA(ppl)I.

Envelope format: letsA(ppl)I docs/APPLYAI_HANDOFF_CONTRACT.md §3 (v1.x).
Route behavior:  docs/phase6_route_contracts.md.

Everything in an envelope is untrusted. This module only checks shape and
limits; it never interprets the content.
"""

from __future__ import annotations

import json
import re
import secrets
import threading
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

MAX_ENVELOPE_BYTES = 64 * 1024
MAX_TEXT_CHARS = 4000
MAX_SHORT_TEXT_CHARS = 300
MAX_EVIDENCE_CHARS = 500
MAX_EVIDENCE_ITEMS = 10
MAX_REQUIREMENTS = 50
MAX_CAPABILITIES = 7
MAX_PROJECTS = 7

PENDING_TTL_SECONDS = 5 * 60
MAX_PENDING = 100

MODALITIES = {"required", "preferred", "optional"}
CONFIDENCE_LEVELS = {"LOW", "MEDIUM", "HIGH"}

_VERSION_RE = re.compile(r"^1\.(0|[1-9][0-9]*)$")


class HandoffValidationError(ValueError):
    """Raised with a short, user-safe reason when an envelope is rejected."""


class HandoffTooLargeError(HandoffValidationError):
    pass


# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------

def _require_keys(obj: Any, required: set, where: str) -> Dict[str, Any]:
    if not isinstance(obj, dict):
        raise HandoffValidationError(f"{where} must be an object")
    keys = set(obj.keys())
    unknown = keys - required
    if unknown:
        raise HandoffValidationError(f"{where} has unknown keys: {', '.join(sorted(unknown))}")
    missing = required - keys
    if missing:
        raise HandoffValidationError(f"{where} is missing keys: {', '.join(sorted(missing))}")
    return obj


def _text(value: Any, where: str, max_chars: int = MAX_TEXT_CHARS, allow_empty: bool = False) -> str:
    if not isinstance(value, str):
        raise HandoffValidationError(f"{where} must be text")
    if not allow_empty and not value.strip():
        raise HandoffValidationError(f"{where} must not be empty")
    if len(value) > max_chars:
        raise HandoffValidationError(f"{where} is longer than {max_chars} characters")
    return value


def _list(value: Any, where: str, min_items: int, max_items: int) -> List[Any]:
    if not isinstance(value, list):
        raise HandoffValidationError(f"{where} must be a list")
    if not (min_items <= len(value) <= max_items):
        raise HandoffValidationError(f"{where} must have {min_items}–{max_items} items")
    return value


def _evidence(value: Any, where: str) -> List[str]:
    items = _list(value, where, 1, MAX_EVIDENCE_ITEMS)
    return [_text(v, f"{where}[{i}]", MAX_EVIDENCE_CHARS) for i, v in enumerate(items)]


def _https_url(value: Any, where: str) -> str:
    url = _text(value, where, 2000)
    if not url.startswith("https://") or any(c.isspace() for c in url):
        raise HandoffValidationError(f"{where} must be an https:// URL")
    return url


def _iso_timestamp(value: Any, where: str) -> str:
    text = _text(value, where, 64)
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        raise HandoffValidationError(f"{where} must be an ISO-8601 timestamp")
    return text


def validate_envelope(data: Any) -> Dict[str, Any]:
    """
    Validate a parsed envelope. Returns a clean copy containing only
    allowlisted fields. Raises HandoffValidationError on any problem.
    """
    env = _require_keys(data, {"handoff_version", "handoff_id", "source", "role", "framing"}, "envelope")

    version = _text(env["handoff_version"], "handoff_version", 16)
    if not _VERSION_RE.match(version):
        raise HandoffValidationError("handoff_version is not supported (expected 1.x)")

    handoff_id = _text(env["handoff_id"], "handoff_id", 64)

    src = _require_keys(env["source"], {
        "system", "job_id", "company", "title", "job_url",
        "interpretation_schema_version", "interpreted_at",
    }, "source")
    if src["system"] != "letsappli":
        raise HandoffValidationError("source.system must be letsappli")

    role = _require_keys(env["role"], {
        "summary_text", "explicit_requirements", "capability_emphasis",
        "project_opportunities", "structural_notes", "confidence",
    }, "role")

    requirements = []
    for i, r in enumerate(_list(role["explicit_requirements"], "role.explicit_requirements", 0, MAX_REQUIREMENTS)):
        where = f"role.explicit_requirements[{i}]"
        r = _require_keys(r, {"requirement_text", "modality"}, where)
        if r["modality"] not in MODALITIES:
            raise HandoffValidationError(f"{where}.modality must be one of {', '.join(sorted(MODALITIES))}")
        requirements.append({
            "requirement_text": _text(r["requirement_text"], f"{where}.requirement_text"),
            "modality": r["modality"],
        })

    capabilities = []
    for i, c in enumerate(_list(role["capability_emphasis"], "role.capability_emphasis", 1, MAX_CAPABILITIES)):
        where = f"role.capability_emphasis[{i}]"
        c = _require_keys(c, {"domain_label", "description", "evidence"}, where)
        capabilities.append({
            "domain_label": _text(c["domain_label"], f"{where}.domain_label", MAX_SHORT_TEXT_CHARS),
            "description": _text(c["description"], f"{where}.description"),
            "evidence": _evidence(c["evidence"], f"{where}.evidence"),
        })

    projects = []
    for i, p in enumerate(_list(role["project_opportunities"], "role.project_opportunities", 0, MAX_PROJECTS)):
        where = f"role.project_opportunities[{i}]"
        p = _require_keys(p, {"capability_surface", "description", "evidence"}, where)
        projects.append({
            "capability_surface": _text(p["capability_surface"], f"{where}.capability_surface", MAX_SHORT_TEXT_CHARS),
            "description": _text(p["description"], f"{where}.description"),
            "evidence": _evidence(p["evidence"], f"{where}.evidence"),
        })

    if role["confidence"] not in CONFIDENCE_LEVELS:
        raise HandoffValidationError("role.confidence must be LOW, MEDIUM, or HIGH")

    return {
        "handoff_version": version,
        "handoff_id": handoff_id,
        "source": {
            "system": "letsappli",
            "job_id": _text(src["job_id"], "source.job_id", MAX_SHORT_TEXT_CHARS),
            "company": _text(src["company"], "source.company", MAX_SHORT_TEXT_CHARS),
            "title": _text(src["title"], "source.title", MAX_SHORT_TEXT_CHARS),
            "job_url": _https_url(src["job_url"], "source.job_url"),
            "interpretation_schema_version": _text(
                src["interpretation_schema_version"], "source.interpretation_schema_version", 32
            ),
            "interpreted_at": _iso_timestamp(src["interpreted_at"], "source.interpreted_at"),
        },
        "role": {
            "summary_text": _text(role["summary_text"], "role.summary_text"),
            "explicit_requirements": requirements,
            "capability_emphasis": capabilities,
            "project_opportunities": projects,
            "structural_notes": _text(role["structural_notes"], "role.structural_notes"),
            "confidence": role["confidence"],
        },
        "framing": _text(env["framing"], "framing", MAX_SHORT_TEXT_CHARS),
    }


def parse_envelope(raw: Optional[str]) -> Dict[str, Any]:
    """Parse and validate the `envelope` form field."""
    if raw is None or not raw.strip():
        raise HandoffValidationError("No envelope was sent")
    if len(raw.encode("utf-8")) > MAX_ENVELOPE_BYTES:
        raise HandoffTooLargeError("Envelope is larger than 64 KB")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise HandoffValidationError("Envelope is not valid JSON")
    return validate_envelope(data)


# ------------------------------------------------------------
# Pending handoffs (token → envelope), in memory only
# ------------------------------------------------------------

class PendingHandoffStore:
    """
    Holds validated envelopes between the cross-site POST and the user's
    accept. Single-use tokens, short expiry, bounded size, never on disk.
    """

    def __init__(
        self,
        ttl_seconds: int = PENDING_TTL_SECONDS,
        max_pending: int = MAX_PENDING,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._ttl = ttl_seconds
        self._max = max_pending
        self._clock = clock
        self._items: Dict[str, Tuple[Dict[str, Any], float]] = {}
        self._lock = threading.Lock()

    def _expired(self, created_at: float) -> bool:
        return self._clock() - created_at > self._ttl

    def _purge_expired(self) -> None:
        for token in [t for t, (_, c) in self._items.items() if self._expired(c)]:
            del self._items[token]

    def park(self, envelope: Dict[str, Any]) -> str:
        token = secrets.token_urlsafe(32)
        with self._lock:
            self._purge_expired()
            while len(self._items) >= self._max:
                oldest = min(self._items, key=lambda t: self._items[t][1])
                del self._items[oldest]
            self._items[token] = (envelope, self._clock())
        return token

    def peek(self, token: str) -> Optional[Dict[str, Any]]:
        """Read without consuming. Returns None if unknown or expired."""
        with self._lock:
            entry = self._items.get(token)
            if entry is None:
                return None
            if self._expired(entry[1]):
                del self._items[token]
                return None
            return entry[0]

    def take(self, token: str) -> Optional[Dict[str, Any]]:
        """Consume. Returns None if unknown, expired, or already taken."""
        with self._lock:
            entry = self._items.pop(token, None)
            if entry is None or self._expired(entry[1]):
                return None
            return entry[0]

    def discard(self, token: str) -> None:
        with self._lock:
            self._items.pop(token, None)

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)
