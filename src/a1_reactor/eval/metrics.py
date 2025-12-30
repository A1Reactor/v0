from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import numpy as np
from PIL import Image

@dataclass
class ConsistencyScore:
    mean_l1: float
    p95_l1: float
    note: str

def _load(path: Path) -> np.ndarray:
    img = Image.open(path).convert("RGB")
    return np.asarray(img).astype("float32") / 255.0

def frame_l1(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean(np.abs(a - b)))

def temporal_consistency(frame_paths: List[Path]) -> ConsistencyScore:
    if len(frame_paths) < 2:
        return ConsistencyScore(0.0, 0.0, "not enough frames")
    diffs = []
    prev = _load(frame_paths[0])
    for p in frame_paths[1:]:
        cur = _load(p)
        diffs.append(frame_l1(prev, cur))
        prev = cur
    diffs_np = np.array(diffs, dtype="float32")
    return ConsistencyScore(
        mean_l1=float(diffs_np.mean()),
        p95_l1=float(np.percentile(diffs_np, 95)),
        note="lower is typically better; interpret with motion level in mind",
    )
