# API

Base URL: `http://localhost:8080`

## POST /v1/jobs
Creates a job and runs it synchronously (prototype behavior).

Request:
```json
{
  "prompt": "cinematic shot",
  "seconds": 2.0,
  "fps": 24,
  "seed": 0,
  "width": 768,
  "height": 768,
  "style_preset": "cinematic",
  "regen_windows": [[0.8, 1.6]]
}
```

Response:
```json
{ "id": "abc123", "status": "done", "artifact_path": "...", "message": null }
```

## GET /v1/jobs/{id}
Returns job status.

## GET /v1/jobs/{id}/artifact
Downloads `artifact.mp4` (if present).
