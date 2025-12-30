from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

class FFmpegError(RuntimeError):
    pass

def encode_video_from_frames(frame_dir: Path, out_path: Path, fps: int = 24, ffmpeg: str = "ffmpeg") -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pattern = str(frame_dir / "%06d.png")
    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out_path),
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise FFmpegError(p.stderr.strip() or "ffmpeg failed")

def has_ffmpeg(ffmpeg: str = "ffmpeg") -> bool:
    try:
        p = subprocess.run([ffmpeg, "-version"], capture_output=True, text=True)
        return p.returncode == 0
    except Exception:
        return False
