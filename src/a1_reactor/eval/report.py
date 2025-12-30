from __future__ import annotations

from pathlib import Path
from typing import Dict, Any
from a1_reactor.eval.metrics import temporal_consistency
from a1_reactor.media.frames import list_frames
from a1_reactor.utils.jsonio import write_json

def make_report(frame_dir: Path, fps: int, out_json: Path) -> Dict[str, Any]:
    frames = list_frames(frame_dir, fps=fps)
    paths = [Path(f.path) for f in frames]
    score = temporal_consistency(paths)
    report = {
        "fps": fps,
        "num_frames": len(paths),
        "temporal_consistency": {
            "mean_l1": score.mean_l1,
            "p95_l1": score.p95_l1,
            "note": score.note,
        },
    }
    write_json(out_json, report)
    return report
