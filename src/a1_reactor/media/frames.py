from __future__ import annotations

from pathlib import Path
from typing import List
from a1_reactor.types import Frame

def frame_name(i: int) -> str:
    return f"{i:06d}.png"

def list_frames(frame_dir: Path, fps: int) -> List[Frame]:
    files = sorted(frame_dir.glob("*.png"))
    frames: List[Frame] = []
    for i, f in enumerate(files):
        frames.append(Frame(index=i, path=str(f), timestamp_s=i / fps))
    return frames
