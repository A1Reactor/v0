from __future__ import annotations

import uuid
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from a1_reactor.config import ReactorConfig
from a1_reactor.engine.engine import ReactorEngine
from a1_reactor.providers.mock import MockProvider
from a1_reactor.providers.http_provider import HTTPProvider
from a1_reactor.server.models import JobCreate, JobStatus
from a1_reactor.types import JobSpec
from a1_reactor.logging import setup_logging
from a1_reactor.storage.db import JobDB

setup_logging()

app = FastAPI(title="A1 Reactor API", version="0.2.0")

CFG = ReactorConfig(db_path=Path(".a1r/jobs.sqlite"))
DB = JobDB(CFG.db_path) if CFG.db_path else None
JOBS: Dict[str, JobStatus] = {}

def _engine_for(payload: JobCreate) -> ReactorEngine:
    if payload.provider == "http":
        if not payload.http_endpoint:
            raise HTTPException(400, "http_endpoint required for provider=http")
        provider = HTTPProvider(payload.http_endpoint)
    else:
        provider = MockProvider()
    return ReactorEngine(CFG, provider=provider)

@app.post("/v1/jobs", response_model=JobStatus)
def create_job(payload: JobCreate):
    jid = uuid.uuid4().hex[:12]
    JOBS[jid] = JobStatus(id=jid, status="queued")
    created_at = datetime.now(timezone.utc).isoformat()

    spec = JobSpec(
        prompt=payload.prompt,
        seconds=payload.seconds,
        fps=payload.fps,
        seed=payload.seed,
        width=payload.width,
        height=payload.height,
        style_preset=payload.style_preset,
        regen_windows=payload.regen_windows,
        metadata={"source": "api", "provider": payload.provider},
    )

    if DB:
        DB.upsert(jid, created_at, "queued", payload.prompt, json.dumps(spec.__dict__, ensure_ascii=False))

    try:
        engine = _engine_for(payload)
        artifact = engine.run(spec)
        JOBS[jid] = JobStatus(id=jid, status="done", artifact_path=str(artifact))
        if DB:
            DB.upsert(jid, created_at, "done", payload.prompt, json.dumps(spec.__dict__, ensure_ascii=False), artifact_path=str(artifact))
    except Exception as e:
        JOBS[jid] = JobStatus(id=jid, status="error", message=str(e))
        if DB:
            DB.upsert(jid, created_at, "error", payload.prompt, json.dumps(spec.__dict__, ensure_ascii=False), error=str(e))

    return JOBS[jid]

@app.get("/v1/jobs/{job_id}", response_model=JobStatus)
def get_job(job_id: str):
    if job_id in JOBS:
        return JOBS[job_id]
    if DB:
        row = DB.get(job_id)
        if row:
            _id, _created, status, _prompt, _spec, artifact, err = row
            return JobStatus(id=_id, status=status, artifact_path=artifact, message=err)
    raise HTTPException(404, "job not found")

@app.get("/v1/jobs/{job_id}/artifact")
def get_artifact(job_id: str):
    js = get_job(job_id)
    if js.status != "done" or not js.artifact_path:
        raise HTTPException(404, "artifact not available")
    p = Path(js.artifact_path)
    if not p.exists():
        raise HTTPException(404, "artifact missing on disk")
    return FileResponse(str(p), filename=p.name, media_type="video/mp4")
