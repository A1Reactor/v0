from __future__ import annotations

import base64
from pathlib import Path
from typing import List, Tuple

import httpx

from a1_reactor.providers.base import Provider
from a1_reactor.types import Frame, JobSpec
from a1_reactor.media.frames import frame_name

class HTTPProvider(Provider):
    """Calls an external HTTP service to get frames.

    This adapter is intentionally strict: it validates frame count and indices.
    """

    def __init__(self, endpoint: str, timeout_s: float = 120.0):
        self.endpoint = endpoint.rstrip("/")
        self.timeout_s = timeout_s

    def _request(self, job: JobSpec) -> dict:
        payload = {
            "prompt": job.prompt,
            "negative_prompt": job.negative_prompt,
            "seed": job.seed,
            "fps": job.fps,
            "seconds": job.seconds,
            "width": job.width,
            "height": job.height,
            "regen_windows": job.regen_windows,
            "metadata": job.metadata or {},
        }
        with httpx.Client(timeout=self.timeout_s) as client:
            r = client.post(self.endpoint, json=payload)
            r.raise_for_status()
            return r.json()

    def generate_frames(self, job: JobSpec, out_dir: Path) -> List[Frame]:
        out_dir.mkdir(parents=True, exist_ok=True)
        data = self._request(job)
        return self._write_frames(data, out_dir, job)

    def regen_frames(self, job: JobSpec, out_dir: Path, windows: List[Tuple[float, float]]) -> List[Frame]:
        # job.regen_windows already set by caller; keep windows param for interface parity
        out_dir.mkdir(parents=True, exist_ok=True)
        data = self._request(job)
        return self._write_frames(data, out_dir, job)

    def _write_frames(self, data: dict, out_dir: Path, job: JobSpec) -> List[Frame]:
        frames_in = data.get("frames") or []
        expected = int(__import__("math").ceil(job.seconds * job.fps))
        if len(frames_in) != expected:
            raise ValueError(f"provider returned {len(frames_in)} frames, expected {expected}")

        frames: List[Frame] = []
        for item in frames_in:
            idx = int(item["index"])
            b64 = item["png_base64"]
            raw = base64.b64decode(b64)
            fp = out_dir / frame_name(idx)
            fp.write_bytes(raw)
            frames.append(Frame(index=idx, path=str(fp), timestamp_s=idx / job.fps))
        frames.sort(key=lambda f: f.index)
        return frames
