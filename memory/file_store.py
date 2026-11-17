from typing import List
from datetime import datetime, timezone

from phase5.memory import (
    MemoryItem,
    MemoryNotFoundError,
    MemoryOwnershipError,
    MemorySource,
)
from .storage import (
    load_memory,
    save_memory,
)


def _parse_ts(value):
    """
    Read a stored timestamp.

    v1 records store ISO-8601 strings. v0 records (written by the old
    approve route) stored Unix floats. Both are read as UTC datetimes.
    Missing or unreadable values return None; they are never replaced
    with "now", because that would misreport when memory was created.
    """
    if isinstance(value, str):
        return datetime.fromisoformat(value)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    return None


def _source_type_from_dict(data: dict) -> str:
    # v1: {"source": {"source_type": ...}}; v0: top-level "source_type".
    source = data.get("source")
    if isinstance(source, dict) and source.get("source_type"):
        return source["source_type"]
    return data.get("source_type") or "legacy"


def _item_from_dict(data: dict) -> MemoryItem:
    return MemoryItem(
        id=data["id"],
        owner_id=data.get("owner_id"),  # legacy-safe
        text=data["text"],
        kind=data.get("kind", "UNKNOWN"),
        source=MemorySource(source_type=_source_type_from_dict(data)),
        created_at=_parse_ts(data.get("created_at")),
        updated_at=_parse_ts(data.get("updated_at")),
        status=data.get("status", "active"),
        deleted_at=_parse_ts(data.get("deleted_at")),
    )

def _item_to_dict(item: MemoryItem) -> dict:
    return {
        "id": item.id,
        "owner_id": item.owner_id,
        "text": item.text,
        "kind": item.kind.value if hasattr(item.kind, "value") else item.kind,
        "source": {
            "source_type": item.source.source_type,
        },
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat(),
        "status": item.status,
        "deleted_at": (
            item.deleted_at.isoformat()
            if item.deleted_at
            else None
        ),
    }


class FileBackedMemoryStore:
    """
    File-backed implementation of the Phase 5.4 memory store.

    Mirrors InMemoryMemoryStore behavior,
    but persists data per owner_id.
    """

    def list(self, owner_id: str) -> List[MemoryItem]:
        raw = load_memory(owner_id)
        items = [_item_from_dict(d) for d in raw]
        return [i for i in items if i.status == "active"]

    def get(self, owner_id: str, memory_id: str, include_deleted: bool = False):
        raw = load_memory(owner_id)
        for d in raw:
            item = _item_from_dict(d)
            if item.id == memory_id:
                if item.status == "deleted" and not include_deleted:
                    return None
                return item
        return None

    def create(self, item: MemoryItem) -> MemoryItem:
        raw = load_memory(item.owner_id)
        raw.append(_item_to_dict(item))
        save_memory(item.owner_id, raw)
        return item

    def delete(self, owner_id: str, memory_id: str) -> None:
        raw = load_memory(owner_id)

        for d in raw:
            if d["id"] == memory_id:
                if d.get("owner_id", owner_id) != owner_id:
                    raise MemoryOwnershipError("owner_id mismatch")

                if d.get("status") == "deleted":
                    return  # idempotent

                now = datetime.now(timezone.utc).isoformat()
                d["status"] = "deleted"
                d["deleted_at"] = now
                d["updated_at"] = now

                save_memory(owner_id, raw)
                return

        raise MemoryNotFoundError(f"Memory item not found: {memory_id}")


