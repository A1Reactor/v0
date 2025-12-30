from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

@dataclass(frozen=True)
class Window:
    start_s: float
    end_s: float

def normalize_windows(windows: Iterable[Tuple[float, float]], seconds: float) -> List[Window]:
    cleaned: List[Tuple[float, float]] = []
    for a, b in windows:
        a2, b2 = max(0.0, float(a)), min(seconds, float(b))
        if b2 <= a2:
            continue
        cleaned.append((a2, b2))
    cleaned.sort()
    merged: List[Window] = []
    for a, b in cleaned:
        if not merged or a > merged[-1].end_s:
            merged.append(Window(a, b))
        else:
            merged[-1] = Window(merged[-1].start_s, max(merged[-1].end_s, b))
    return merged
