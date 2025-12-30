from __future__ import annotations

from pathlib import Path
import shutil
from typing import Optional

def export_artifact(artifact: Path, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(artifact, out_path)
    return out_path

def export_run_dir(run_dir: Path, out_dir: Path, *, include_frames: bool = False) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in run_dir.rglob("*"):
        if p.is_dir():
            continue
        if (p.suffix.lower() == ".png") and (not include_frames):
            continue
        rel = p.relative_to(run_dir)
        dst = out_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)
    return out_dir
