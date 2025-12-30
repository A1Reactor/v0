from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

@dataclass
class PromptDSL:
    fields: Dict[str, str]

    @staticmethod
    def parse(text: str) -> "PromptDSL":
        fields: Dict[str, str] = {}
        # very small DSL: key:value tokens
        for tok in text.split():
            if ":" not in tok:
                continue
            k, v = tok.split(":", 1)
            fields[k.strip().lower()] = v.strip().strip('"')
        return PromptDSL(fields)

    def to_prompt(self) -> str:
        # stable order for reproducibility
        priority = ["subject", "style", "lens", "motion", "light", "bg"]
        parts: List[str] = []
        for k in priority:
            if k in self.fields:
                parts.append(f"{k} {self.fields[k]}")
        for k, v in sorted(self.fields.items()):
            if k in priority:
                continue
            parts.append(f"{k} {v}")
        return ", ".join(parts)
