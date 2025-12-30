from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

@dataclass
class BlendConfig:
    enabled: bool = False
    # number of frames to crossfade at the boundary (provider-dependent)
    boundary_frames: int = 2

def should_blend(cfg: Optional[BlendConfig]) -> bool:
    return bool(cfg and cfg.enabled and cfg.boundary_frames > 0)
