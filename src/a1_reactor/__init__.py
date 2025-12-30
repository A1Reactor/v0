"""A1 Reactor package.

This repository is a prototype of a generation/regen pipeline. The included provider defaults
to MockProvider for deterministic local demos.
"""

from .config import ReactorConfig
from .engine.engine import ReactorEngine

__all__ = ["ReactorConfig", "ReactorEngine"]
