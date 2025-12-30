from __future__ import annotations

import math
from pathlib import Path
from typing import List, Tuple

from a1_reactor.providers.base import Provider
from a1_reactor.types import Frame, JobSpec
from a1_reactor.media.frames import frame_name
from a1_reactor.media.images import make_debug_frame, save_png

class MockProvider(Provider):
    """A deterministic placeholder provider.

    This is intentionally 'fake generation' for pipeline development. It creates noisy frames
    with labels so you can test regen windows and stitching.
    """

    def generate_frames(self, job: JobSpec, out_dir: Path) -> List[Frame]:
        out_dir.mkdir(parents=True, exist_ok=True)
        n = int(math.ceil(job.seconds * job.fps))
        frames: List[Frame] = []
        for i in range(n):
            img = make_debug_frame(job.width, job.height, f"A1 Reactor\nMOCK GEN\n{i}/{n}\nseed={job.seed}", seed=job.seed + i)
            fp = out_dir / frame_name(i)
            save_png(img, fp)
            frames.append(Frame(index=i, path=str(fp), timestamp_s=i / job.fps))
        return frames

    def regen_frames(self, job: JobSpec, out_dir: Path, windows: List[Tuple[float, float]]) -> List[Frame]:
        out_dir.mkdir(parents=True, exist_ok=True)
        n = int(math.ceil(job.seconds * job.fps))
        frames: List[Frame] = []
        for i in range(n):
            t = i / job.fps
            in_win = any(a <= t <= b for a, b in windows)
            tag = "REGEN" if in_win else "KEEP"
            seed = (job.seed + i) if not in_win else (job.seed + 10000 + i)
            img = make_debug_frame(job.width, job.height, f"A1 Reactor\nMOCK {tag}\n{i}/{n}\nseed={seed}", seed=seed)
            fp = out_dir / frame_name(i)
            save_png(img, fp)
            frames.append(Frame(index=i, path=str(fp), timestamp_s=t))
        return frames
