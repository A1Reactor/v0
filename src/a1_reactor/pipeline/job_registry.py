from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
import threading
import time

@dataclass
class JobRecord:
    id: str
    status: str
    created_at: float
    updated_at: float
    message: Optional[str] = None
    artifact_path: Optional[str] = None

class JobRegistry:
    """Thread-safe in-memory registry for prototype deployments."""

    def __init__(self):
        self._lock = threading.Lock()
        self._jobs: Dict[str, JobRecord] = {}

    def put(self, rec: JobRecord) -> None:
        with self._lock:
            self._jobs[rec.id] = rec

    def get(self, job_id: str) -> Optional[JobRecord]:
        with self._lock:
            return self._jobs.get(job_id)

    def touch(self, job_id: str, *, status: Optional[str]=None, message: Optional[str]=None,
              artifact_path: Optional[str]=None) -> None:
        with self._lock:
            rec = self._jobs.get(job_id)
            if not rec:
                return
            if status is not None:
                rec.status = status
            if message is not None:
                rec.message = message
            if artifact_path is not None:
                rec.artifact_path = artifact_path
            rec.updated_at = time.time()

    def cleanup_older_than(self, seconds: float) -> int:
        now = time.time()
        removed = 0
        with self._lock:
            for k in list(self._jobs.keys()):
                if now - self._jobs[k].updated_at > seconds:
                    del self._jobs[k]
                    removed += 1
        return removed
