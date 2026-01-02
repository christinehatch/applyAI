# telemetry.py
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional


def _now_ts() -> float:
    return time.time()


def _safe_git_sha() -> Optional[str]:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return None


class EventLogger:
    """
    Local-only structured event logging. Designed for:
    - comparing runs over time
    - replaying the same input cases
    - tracking behavior drift across commits
    """

    def __init__(self, enabled: bool, base_dir: Path) -> None:
        self.enabled = enabled
        self.base_dir = base_dir
        run_id = os.getenv("CAREER_EXPLORER_RUN_ID")
        if not run_id:
            run_id = f"run-{int(_now_ts())}-{uuid.uuid4().hex[:8]}"
            os.environ["CAREER_EXPLORER_RUN_ID"] = run_id

        self.run_id = run_id
        self.git_sha = _safe_git_sha()

        if not self.enabled:
            return

        self.run_dir = self.base_dir / "runs" / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)

        self.events_path = self.run_dir / "events.jsonl"
        self.sessions_dir = self.run_dir / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

        meta = {
            "run_id": self.run_id,
            "started_at": _now_ts(),
            "git_sha": self.git_sha,
            "python": sys.version,
            "platform": platform.platform(),
            "argv": sys.argv,
        }
        meta_path = self.run_dir / "run_meta.json"
        if not meta_path.exists():
            meta_path.write_text(json.dumps(meta, indent=2))

    def event(self, session_id: str, event_type: str, payload: Optional[Dict[str, Any]] = None) -> None:
        if not self.enabled:
            return

        record = {
            "ts": _now_ts(),
            "run_id": self.run_id,
            "git_sha": self.git_sha,
            "session_id": session_id,
            "type": event_type,
            "payload": payload or {},
        }
        with self.events_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def write_session_snapshot(self, session_id: str, snapshot: Dict[str, Any]) -> Path:
        """
        Write a single JSON snapshot for convenient diff/replay.
        """
        if not self.enabled:
            return Path()

        path = self.sessions_dir / f"{session_id}.json"
        enriched = {
            "run_id": self.run_id,
            "git_sha": self.git_sha,
            "session_id": session_id,
            "snapshot_ts": _now_ts(),
            "data": snapshot,
        }
        path.write_text(json.dumps(enriched, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

