from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

@dataclass(frozen=True)
class Frame:
    index: int
    path: str
    timestamp_s: float

@dataclass
class JobSpec:
    prompt: str
    negative_prompt: str = ""
    seed: int = 0
    fps: int = 24
    seconds: float = 2.0
    width: int = 768
    height: int = 768
    style_preset: Optional[str] = None
    regen_windows: Optional[List[Tuple[float, float]]] = None
    metadata: Dict[str, Any] | None = None
