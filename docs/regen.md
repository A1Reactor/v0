# Regeneration (Regen)

Regen is the ability to **rebuild part of a clip**.

A1 Reactor represents regen as **time windows** in seconds:
- `[[start_s, end_s], ...]`

The provider decides how to apply regen:
- local model might use anchors/latents
- hosted model might accept frame hints
- mock provider stamps frames as KEEP/REGEN

A1 Reactor handles:
- window normalization / merging
- file layout and metadata
- boundary hooks for blending (pluggable)

See:
- `src/a1_reactor/engine/windows.py`
- `src/a1_reactor/providers/base.py`
