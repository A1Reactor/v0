from __future__ import annotations

import logging
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from a1_reactor.config import ReactorConfig
from a1_reactor.engine.cache import ArtifactCache
from a1_reactor.engine.windows import normalize_windows
from a1_reactor.prompts.normalize import normalize_prompt
from a1_reactor.prompts.presets import apply_preset
from a1_reactor.providers.base import Provider
from a1_reactor.types import JobSpec
from a1_reactor.media.ffmpeg import encode_video_from_frames
from a1_reactor.media.frames import list_frames
from a1_reactor.eval.report import make_report
from a1_reactor.utils.jsonio import write_json
from a1_reactor.utils.time import timed

log = logging.getLogger(__name__)

class ReactorEngine:
    def __init__(self, cfg: ReactorConfig, provider: Provider):
        self.cfg = cfg
        self.provider = provider
        self.cfg.ensure()
        cache_root = cfg.cache_dir or (cfg.workspace / "cache")
        self.cache = ArtifactCache(cache_root)

    def run(self, job: JobSpec, *, force: bool = False) -> Path:
        # normalize + presets
        job.prompt = normalize_prompt(job.prompt)
        merged, neg = apply_preset(job.prompt, job.style_preset)
        job.prompt, job.negative_prompt = merged, neg
        if job.seed == 0:
            job.seed = self.cfg.default_seed

        spec = asdict(job)
        meta_path = self.cache.meta_path(spec)
        run_dir = self.cache.run_dir(spec)
        frames_dir = run_dir / "frames"
        artifact = self.cache.artifact_path(spec)

        if not force:
            existing = self.cache.get_existing_artifact(spec)
            if existing:
                return existing

        write_json(meta_path, spec)

        with timed("provider", log=log.info):
            if job.regen_windows:
                windows = normalize_windows(job.regen_windows, job.seconds)
                frames = self.provider.regen_frames(job, frames_dir, [(w.start_s, w.end_s) for w in windows])
            else:
                frames = self.provider.generate_frames(job, frames_dir)

        with timed("stitch", log=log.info):
            encode_video_from_frames(frames_dir, artifact, fps=job.fps, ffmpeg=self.cfg.ffmpeg_path)

        # report
        try:
            with timed("report", log=log.info):
                make_report(frames_dir, fps=job.fps, out_json=run_dir / "report.json")
        except Exception as e:
            log.warning(f"report failed: {e}")

        return artifact
