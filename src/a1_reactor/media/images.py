from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

def make_debug_frame(width: int, height: int, text: str, seed: int) -> Image.Image:
    rng = np.random.default_rng(seed)
    arr = (rng.random((height, width, 3)) * 28 + 12).astype("uint8")
    img = Image.fromarray(arr, mode="RGB")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width - 1, height - 1], outline=(200, 200, 200))
    d.text((16, 16), text, fill=(240, 240, 240))
    return img

def save_png(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG", optimize=True)
