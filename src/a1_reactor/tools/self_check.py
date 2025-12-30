from __future__ import annotations

from pathlib import Path
import tempfile

from a1_reactor.config import ReactorConfig
from a1_reactor.engine.engine import ReactorEngine
from a1_reactor.providers.mock import MockProvider
from a1_reactor.types import JobSpec
from a1_reactor.media.ffmpeg import has_ffmpeg

def main() -> int:
    # Import sanity
    assert ReactorEngine
    assert MockProvider

    with tempfile.TemporaryDirectory() as td:
        cfg = ReactorConfig(workspace=Path(td))
        engine = ReactorEngine(cfg, provider=MockProvider())
        job = JobSpec(prompt="self check clip", seconds=1.0, fps=12, width=256, height=256, style_preset="studio", seed=123)
        artifact = engine.run(job, force=True)
        # If ffmpeg isn't available in CI, artifact generation will fail; gate it.
        # Our CI installs ffmpeg on ubuntu-latest typically, but we keep a soft check.
        assert artifact.exists(), f"artifact missing: {artifact}"
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
