from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

@dataclass
class ReactorConfig:
    workspace: Path = field(default_factory=lambda: Path(".a1r"))
    ffmpeg_path: str = "ffmpeg"
    ffprobe_path: str = "ffprobe"
    default_fps: int = 24
    default_seed: int = 1337
    cache_dir: Optional[Path] = None
    db_path: Optional[Path] = None

    def ensure(self) -> None:
        self.workspace.mkdir(parents=True, exist_ok=True)
        (self.workspace / "cache").mkdir(parents=True, exist_ok=True)
        (self.workspace / "runs").mkdir(parents=True, exist_ok=True)
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        if self.db_path:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
