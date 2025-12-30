from __future__ import annotations

from pathlib import Path
from typing import Tuple
import numpy as np
from PIL import Image

def image_diff(a_path: Path, b_path: Path) -> Tuple[float, float]:
    """Return (mean_abs, max_abs) diff in [0..1]."""
    a = np.asarray(Image.open(a_path).convert("RGB")).astype("float32") / 255.0
    b = np.asarray(Image.open(b_path).convert("RGB")).astype("float32") / 255.0
    d = np.abs(a - b)
    return float(d.mean()), float(d.max())
