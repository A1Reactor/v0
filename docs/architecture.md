# Architecture

## High-level flow

```text
Prompt -> Normalize -> Presets -> JobSpec
      -> Provider (generate/regen frames)
      -> FrameStore (disk)
      -> Stitch (ffmpeg)
      -> Report (metrics)
      -> Artifact (mp4) + metadata
```

## Module responsibilities
- `engine/`: orchestration, caching, regen windows, blending hooks
- `providers/`: backend adapters (mock, http)
- `media/`: ffmpeg + frame naming + encoding utilities
- `server/`: FastAPI endpoints + job registry
- `storage/`: SQLite metadata store + exports
- `eval/`: metrics + reports
