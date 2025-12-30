from __future__ import annotations

from pathlib import Path
from typing import Optional
from a1_reactor.utils.hashing import stable_hash

class ArtifactCache:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def key(self, spec: dict) -> str:
        return stable_hash(spec)[:16]

    def run_dir(self, spec: dict) -> Path:
        k = self.key(spec)
        d = self.root / k / "run"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def artifact_path(self, spec: dict) -> Path:
        k = self.key(spec)
        d = self.root / k
        d.mkdir(parents=True, exist_ok=True)
        return d / "artifact.mp4"

    def meta_path(self, spec: dict) -> Path:
        k = self.key(spec)
        d = self.root / k
        d.mkdir(parents=True, exist_ok=True)
        return d / "job.json"

    def get_existing_artifact(self, spec: dict) -> Optional[Path]:
        p = self.artifact_path(spec)
        return p if p.exists() else None
