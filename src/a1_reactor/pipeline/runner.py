from __future__ import annotations

import uuid
import time
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from a1_reactor.engine.engine import ReactorEngine
from a1_reactor.pipeline.job_registry import JobRegistry, JobRecord
from a1_reactor.types import JobSpec
from a1_reactor.utils.hashing import stable_hash

class Runner:
    """Small runner abstraction that can later become async/queued."""

    def __init__(self, engine: ReactorEngine, registry: Optional[JobRegistry] = None):
        self.engine = engine
        self.registry = registry or JobRegistry()

    def submit(self, job: JobSpec) -> str:
        jid = uuid.uuid4().hex[:12]
        now = time.time()
        self.registry.put(JobRecord(id=jid, status="queued", created_at=now, updated_at=now))
        return jid

    def run_sync(self, job_id: str, job: JobSpec) -> Path:
        self.registry.touch(job_id, status="running")
        try:
            artifact = self.engine.run(job, force=True)
            self.registry.touch(job_id, status="done", artifact_path=str(artifact))
            return artifact
        except Exception as e:
            self.registry.touch(job_id, status="error", message=str(e))
            raise
