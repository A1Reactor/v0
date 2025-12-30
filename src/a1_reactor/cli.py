from __future__ import annotations

import argparse
from pathlib import Path

from a1_reactor.logging import setup_logging
from a1_reactor.config import ReactorConfig
from a1_reactor.engine.engine import ReactorEngine
from a1_reactor.providers.mock import MockProvider
from a1_reactor.types import JobSpec

def _engine() -> ReactorEngine:
    cfg = ReactorConfig(workspace=Path(".a1r"))
    return ReactorEngine(cfg, provider=MockProvider())

def cmd_demo(args: argparse.Namespace) -> int:
    engine = _engine()
    job = JobSpec(prompt=args.prompt, seconds=args.seconds, fps=args.fps, style_preset=args.preset, seed=args.seed)
    artifact = engine.run(job, force=args.force)
    print(artifact)
    return 0

def cmd_regen(args: argparse.Namespace) -> int:
    engine = _engine()
    windows = []
    for pair in args.regen:
        windows.append((pair[0], pair[1]))
    job = JobSpec(prompt=args.prompt, seconds=args.seconds, fps=args.fps, style_preset=args.preset, seed=args.seed, regen_windows=windows)
    artifact = engine.run(job, force=True)
    print(artifact)
    return 0

def main() -> int:
    setup_logging()
    ap = argparse.ArgumentParser(prog="a1-reactor")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("demo", help="run a demo job (mock provider)")
    p.add_argument("--prompt", required=True)
    p.add_argument("--seconds", type=float, default=2.0)
    p.add_argument("--fps", type=int, default=24)
    p.add_argument("--preset", default="cinematic")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_demo)

    r = sub.add_parser("regen", help="run a regen job with windows")
    r.add_argument("--prompt", required=True)
    r.add_argument("--seconds", type=float, default=3.0)
    r.add_argument("--fps", type=int, default=24)
    r.add_argument("--preset", default="cinematic")
    r.add_argument("--seed", type=int, default=0)
    r.add_argument("--regen", nargs=2, type=float, action="append", required=True, metavar=("START_S","END_S"))
    r.set_defaults(fn=cmd_regen)

    args = ap.parse_args()
    return int(args.fn(args))

if __name__ == "__main__":
    raise SystemExit(main())
