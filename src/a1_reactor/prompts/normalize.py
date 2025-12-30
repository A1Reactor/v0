from __future__ import annotations
import re

_WS = re.compile(r"\s+")

def normalize_prompt(prompt: str) -> str:
    p = prompt.strip()
    p = _WS.sub(" ", p)
    p = p.replace("“", '"').replace("”", '"').replace("’", "'")
    return p
