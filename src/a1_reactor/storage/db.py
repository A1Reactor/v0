from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  status TEXT NOT NULL,
  prompt TEXT NOT NULL,
  spec_json TEXT NOT NULL,
  artifact_path TEXT,
  error TEXT
);
"""

class JobDB:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(str(self.path))

    def _init(self) -> None:
        with self._connect() as cx:
            cx.execute(SCHEMA)

    def upsert(self, job_id: str, created_at: str, status: str, prompt: str, spec_json: str,
               artifact_path: Optional[str] = None, error: Optional[str] = None) -> None:
        with self._connect() as cx:
            cx.execute(
                """INSERT INTO jobs(id, created_at, status, prompt, spec_json, artifact_path, error)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(id) DO UPDATE SET
                     status=excluded.status,
                     artifact_path=excluded.artifact_path,
                     error=excluded.error
                """,
                (job_id, created_at, status, prompt, spec_json, artifact_path, error),
            )

    def get(self, job_id: str) -> Optional[Tuple[Any, ...]]:
        with self._connect() as cx:
            cur = cx.execute("SELECT id, created_at, status, prompt, spec_json, artifact_path, error FROM jobs WHERE id=?", (job_id,))
            return cur.fetchone()
