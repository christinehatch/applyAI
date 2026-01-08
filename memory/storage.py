from pathlib import Path
import json
from typing import List, Dict, Any

BASE_MEMORY_DIR = Path(__file__).resolve().parent

def owner_dir(owner_id: str) -> Path:
    """
    Return the filesystem directory for a given owner_id.

    Does NOT create directories.
    Does NOT read or write files.
    """
    return BASE_MEMORY_DIR / "owners" / owner_id

def ensure_owner_dir(owner_id: str) -> Path:
    """
    Ensure the directory for an owner_id exists.
    Safe to call multiple times.
    """
    path = owner_dir(owner_id)
    path.mkdir(parents=True, exist_ok=True)
    return path

def memory_file(owner_id: str) -> Path:
    """
    Path to the approved, persistent memory file for this owner.

    Does NOT create files.
    Does NOT read or write.
    """
    return owner_dir(owner_id) / "memory.json"


def proposals_file(owner_id: str) -> Path:
    """
    Path to pending memory proposals for this owner.

    Does NOT create files.
    Does NOT read or write.
    """
    return owner_dir(owner_id) / "proposals.json"

def ensure_owner_files(owner_id: str) -> None:
    """
    Explicitly create the owner directory and empty JSON files
    if they do not already exist.

    This function MUST be called intentionally.
    """
    odir = owner_dir(owner_id)
    odir.mkdir(parents=True, exist_ok=True)

    for path in (memory_file(owner_id), proposals_file(owner_id)):
        if not path.exists():
            path.write_text("[]", encoding="utf-8")

def load_memory(owner_id: str) -> List[Dict[str, Any]]:
    """
    Read memory.json for an owner.

    - Read-only
    - Returns [] if file does not exist
    - Does NOT create files
    """
    path = memory_file(owner_id)

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_proposals(owner_id: str) -> List[Dict[str, Any]]:
    """
    Read proposals.json for an owner.

    - Read-only
    - Returns [] if file does not exist
    - Does NOT create files
    """
    path = proposals_file(owner_id)

    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

# Proposal record schema (implicit, storage-owned):
# {
#   proposal_id: str
#   owner_id: str
#   proposed_text: str
#   kind: str
#   source_type: str
#   decision: "pending" | "approved" | "declined"
#   created_at: Optional[float]
#   declined_at?: float
#   decline_reason?: str
# }

def append_proposal(
    owner_id: str,
    proposed_text: str,
    kind: str,
    source_type: str,
) -> None:
    proposals = load_proposals(owner_id)

    proposals.append({
        "proposal_id": str(len(proposals) + 1),
        "owner_id": owner_id,
        "proposed_text": proposed_text,
        "kind": kind,
        "source_type": source_type,
        "decision": "pending",
        "created_at": None  # or time.time() if you prefer
         })

    save_proposals(owner_id, proposals)


def save_memory(owner_id: str, items: list) -> None:
    """
    Overwrite memory.json for an owner.

    - Explicit write
    - Creates owner directory if missing
    - No validation
    - No merging
    """
    owner_path = ensure_owner_dir(owner_id)
    path = memory_file(owner_id)

    with path.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)


def save_proposals(owner_id: str, proposals: list) -> None:
    """
    Overwrite proposals.json for an owner.

    - Explicit write
    - Creates owner directory if missing
    - No validation
    - No merging
    """
    owner_path = ensure_owner_dir(owner_id)
    path = proposals_file(owner_id)

    with path.open("w", encoding="utf-8") as f:
        json.dump(proposals, f, indent=2)

