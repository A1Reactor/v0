from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class RGB:
    r: int
    g: int
    b: int

    def clamp(self) -> "RGB":
        return RGB(
            max(0, min(255, int(self.r))),
            max(0, min(255, int(self.g))),
            max(0, min(255, int(self.b))),
        )

def lerp(a: RGB, b: RGB, t: float) -> RGB:
    t = max(0.0, min(1.0, float(t)))
    return RGB(
        int(a.r + (b.r - a.r) * t),
        int(a.g + (b.g - a.g) * t),
        int(a.b + (b.b - a.b) * t),
    ).clamp()
