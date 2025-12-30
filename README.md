# A1 Reactor

> **A1 Reactor** is a working **prototype** of a video/image *generation + regeneration (“regen”)* pipeline.
> It is **not** a drop-in “secret model.” The repo focuses on the parts that make *iteration* possible:
> job specs, prompt normalization, provider abstraction, frame IO, stitching, simple consistency metrics,
> and an API you can run locally.

---

## Why “regen”?
Most tools generate once. Iteration becomes roulette.

A1 Reactor is designed around regen loops:

1. **Lock** the intent (prompt + seed + anchors)
2. **Target** a window (frames/seconds) to rebuild
3. **Regen** just that region (provider-dependent)
4. **Blend** boundaries to avoid visible seams
5. **Stitch** frames into an artifact (mp4)
6. **Score** temporal consistency (basic metrics)

This repo ships a complete **pipeline skeleton** with a **MockProvider** that makes deterministic placeholder frames,
plus an **HTTPProvider** interface for wiring a real backend (local model server, hosted API, etc).

---

## Features

### Core pipeline
- Job spec → prompt normalization → preset system
- Provider interface: `generate_frames()` + `regen_frames()`
- Deterministic run directories & metadata
- Frame IO helpers + naming conventions
- Stitching via ffmpeg
- Simple temporal consistency scoring + reports

### Developer tooling
- CLI: run demo jobs, regen windows, export artifacts
- FastAPI server: create jobs, query status, download artifact
- SQLite store for job metadata (optional)
- CI workflow + unit tests

### UI (minimal)
- A small static “job submitter” UI in `/ui` (no build step required)

---

## Quick start

### 1) Requirements
- Python 3.10+
- ffmpeg installed (for mp4 stitching)

### 2) Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 3) Run a demo
```bash
python -m a1_reactor.cli demo --prompt "cinematic golden hour street shot, handheld, shallow depth of field"
```

Artifacts are written under:
- `.a1r/cache/<hash>/artifact.mp4`
- `.a1r/cache/<hash>/run/frames/*.png`

### 4) Regen a window
```bash
python -m a1_reactor.cli regen --prompt "same scene but sharper textures" --seconds 3 --regen 0.8 1.6
```

### 5) Start API server
```bash
uvicorn a1_reactor.server.api:app --host 0.0.0.0 --port 8080
```

---

## Using a real backend
The included `MockProvider` generates placeholder frames on purpose.

To hook up a real generator, implement `Provider` (or use `HTTPProvider`):
- `src/a1_reactor/providers/base.py`
- `src/a1_reactor/providers/http_provider.py`

`HTTPProvider` expects a JSON API returning base64 PNG frames (see docs):
- `docs/providers/http-provider.md`

---

## Project layout
- `src/a1_reactor/` — engine, providers, media, eval, server, storage, CLI
- `tests/` — unit tests for core building blocks
- `docs/` — architecture, API, providers, design notes, ADRs
- `examples/` — prompts, job specs, and small datasets
- `ui/` — minimal static web UI to submit jobs to the API
- `scripts/` — demo + utilities

---

## Notes on maturity
This is an **engineering scaffold** meant to be extended.
If you’re evaluating: run the demo, check the API, inspect the provider contracts.

---

## License
MIT — see `LICENSE`

*Created: 2025-12-30*
