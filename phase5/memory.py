from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

from .bounded_adapter import (
    IDENTITY_LOCKING_PHRASES,
    CLINICAL_DIAGNOSTIC_TERMS,
    AUTHORITATIVE_PHRASES,
)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


class MemoryError(Exception):
    """Base class for Phase 5.4 memory errors."""


class MemoryValidationError(MemoryError):
    """Raised when memory text violates storage constraints."""


class MemoryNotFoundError(MemoryError):
    """Raised when a memory item cannot be found."""


class MemoryProposalNotFoundError(MemoryError):
    """Raised when a proposal cannot be found."""


class MemoryProposalStateError(MemoryError):
    """Raised when an invalid proposal state transition is attempted."""


class MemoryOwnershipError(MemoryError):
    """Raised when an owner_id mismatch occurs."""


class MemoryKind(str, Enum):
    PREFERENCE = "PREFERENCE"
    CONSTRAINT = "CONSTRAINT"
    GOAL = "GOAL"
    SELF_OBSERVATION = "SELF_OBSERVATION"


@dataclass(frozen=True)
class MemorySource:
    source_type: str  # "phase3_reflection" | "phase5_3_interpretation"
    source_id: Optional[str] = None
    note: Optional[str] = None


@dataclass
class MemoryItem:
    id: str
    owner_id: str
    text: str
    kind: MemoryKind
    source: MemorySource
    created_at: datetime
    updated_at: datetime
    status: str  # "active" | "deleted"
    deleted_at: Optional[datetime] = None


@dataclass
class MemoryProposal:
    proposal_id: str
    owner_id: str
    proposed_text: str
    kind: MemoryKind
    source: MemorySource
    created_at: datetime
    decision: str  # "pending" | "approved" | "declined"
    decided_at: Optional[datetime] = None
    final_text: Optional[str] = None
    result_memory_id: Optional[str] = None


@dataclass(frozen=True)
class SelectedMemoryContext:
    selected_memory_ids: List[str]
    resolved_texts: List[str]
    attribution_line: str


def validate_memory_text(text: str) -> None:
    """
    Mechanical validator for text that is about to be stored as memory.
    Must enforce: no identity locking, no clinical/diagnostic framing,
    no authoritative/prescriptive language.
    """
    lowered = text.lower()

    for phrase in IDENTITY_LOCKING_PHRASES:
        if phrase in lowered:
            raise MemoryValidationError(f"Identity-locking language detected: '{phrase}'")

    for term in CLINICAL_DIAGNOSTIC_TERMS:
        if term in lowered:
            raise MemoryValidationError(f"Clinical/diagnostic term detected: '{term}'")

    for phrase in AUTHORITATIVE_PHRASES:
        if phrase in lowered:
            raise MemoryValidationError(f"Authoritative/prescriptive language detected: '{phrase}'")


class InMemoryMemoryStore:
    """
    Minimal in-memory store for Phase 5.4 contracts.
    This is intentionally not wired into any runtime flow yet.
    """

    def __init__(self) -> None:
        self._items_by_owner: Dict[str, Dict[str, MemoryItem]] = {}

    def list(self, owner_id: str) -> List[MemoryItem]:
        items = list(self._items_by_owner.get(owner_id, {}).values())
        return [i for i in items if i.status == "active"]

    def get(self, owner_id: str, memory_id: str, include_deleted: bool = False) -> Optional[MemoryItem]:
        item = self._items_by_owner.get(owner_id, {}).get(memory_id)
        if item is None:
            return None
        if item.status == "deleted" and not include_deleted:
            return None
        return item

    def create(self, item: MemoryItem) -> MemoryItem:
        self._items_by_owner.setdefault(item.owner_id, {})
        self._items_by_owner[item.owner_id][item.id] = item
        return item

    def delete(self, owner_id: str, memory_id: str) -> None:
        item = self._items_by_owner.get(owner_id, {}).get(memory_id)
        if item is None:
            raise MemoryNotFoundError(f"Memory item not found: {memory_id}")
        if item.owner_id != owner_id:
            raise MemoryOwnershipError("owner_id mismatch")
        if item.status == "deleted":
            return  # idempotent delete

        item.status = "deleted"
        item.deleted_at = _now_utc()
        item.updated_at = item.deleted_at


class InMemoryMemoryProposalService:
    """
    Minimal proposal workflow: propose -> approve/decline.
    Enforces proposal-before-write and decline-no-side-effects.
    """

    def __init__(self, store: InMemoryMemoryStore) -> None:
        self._store = store
        self._proposals_by_owner: Dict[str, Dict[str, MemoryProposal]] = {}
        self._proposal_counter = 0
        self._memory_counter = 0

    def _next_proposal_id(self) -> str:
        self._proposal_counter += 1
        return f"mp-{self._proposal_counter}"

    def _next_memory_id(self) -> str:
        self._memory_counter += 1
        return f"m-{self._memory_counter}"

    def propose(self, owner_id: str, proposed_text: str, kind: MemoryKind, source: MemorySource) -> MemoryProposal:
        proposal = MemoryProposal(
            proposal_id=self._next_proposal_id(),
            owner_id=owner_id,
            proposed_text=proposed_text,
            kind=kind,
            source=source,
            created_at=_now_utc(),
            decision="pending",
        )
        self._proposals_by_owner.setdefault(owner_id, {})
        self._proposals_by_owner[owner_id][proposal.proposal_id] = proposal
        return proposal

    def approve(self, owner_id: str, proposal_id: str, final_text: str) -> MemoryItem:
        proposal = self._proposals_by_owner.get(owner_id, {}).get(proposal_id)
        if proposal is None:
            raise MemoryProposalNotFoundError(f"Proposal not found: {proposal_id}")
        if proposal.owner_id != owner_id:
            raise MemoryOwnershipError("owner_id mismatch")
        if proposal.decision != "pending":
            raise MemoryProposalStateError(f"Cannot approve proposal in state: {proposal.decision}")

        validate_memory_text(final_text)

        now = _now_utc()
        item = MemoryItem(
            id=self._next_memory_id(),
            owner_id=owner_id,
            text=final_text,
            kind=proposal.kind,
            source=proposal.source,
            created_at=now,
            updated_at=now,
            status="active",
        )
        self._store.create(item)

        proposal.decision = "approved"
        proposal.decided_at = now
        proposal.final_text = final_text
        proposal.result_memory_id = item.id

        return item

    def decline(self, owner_id: str, proposal_id: str) -> None:
        proposal = self._proposals_by_owner.get(owner_id, {}).get(proposal_id)
        if proposal is None:
            raise MemoryProposalNotFoundError(f"Proposal not found: {proposal_id}")
        if proposal.owner_id != owner_id:
            raise MemoryOwnershipError("owner_id mismatch")
        if proposal.decision != "pending":
            raise MemoryProposalStateError(f"Cannot decline proposal in state: {proposal.decision}")

        now = _now_utc()
        proposal.decision = "declined"
        proposal.decided_at = now

        # Decline must have no side effects and should not retain usable text.
        # (If you later add audit logging, keep only decision metadata.)
        proposal.proposed_text = ""
        proposal.final_text = None
        proposal.result_memory_id = None


class MemorySelectionContextBuilder:
    """
    Retrieval guard: resolves ONLY active memory items.
    Never auto-consumes memory; caller must provide selected IDs.
    """

    def __init__(self, store: InMemoryMemoryStore) -> None:
        self._store = store

    def build(self, owner_id: str, selected_memory_ids: List[str]) -> SelectedMemoryContext:
        resolved: List[str] = []
        for mid in selected_memory_ids:
            item = self._store.get(owner_id=owner_id, memory_id=mid, include_deleted=False)
            if item is not None:
                resolved.append(item.text)

        return SelectedMemoryContext(
            selected_memory_ids=list(selected_memory_ids),
            resolved_texts=resolved,
            attribution_line=("Using the items you selected…" if resolved else ""),
        )
