from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple
from a1_reactor.types import Frame, JobSpec

class Provider(ABC):
    @abstractmethod
    def generate_frames(self, job: JobSpec, out_dir: Path) -> List[Frame]:
        raise NotImplementedError

    @abstractmethod
    def regen_frames(self, job: JobSpec, out_dir: Path, windows: List[Tuple[float, float]]) -> List[Frame]:
        raise NotImplementedError
