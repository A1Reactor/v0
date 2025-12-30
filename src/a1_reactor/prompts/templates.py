from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class Template:
    name: str
    text: str

TEMPLATES: Dict[str, Template] = {
    "realistic_cinematic": Template(
        name="realistic_cinematic",
        text="cinematic lighting, shallow depth of field, realistic textures, subtle film grain, {subject}"
    ),
    "product_studio": Template(
        name="product_studio",
        text="soft studio lighting, seamless background, sharp details, {subject}"
    ),
}

def render(name: str, **kwargs) -> str:
    if name not in TEMPLATES:
        raise KeyError(name)
    return TEMPLATES[name].text.format(**kwargs)
