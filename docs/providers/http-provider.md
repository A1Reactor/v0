# HTTP Provider

`HTTPProvider` lets you connect A1 Reactor to a generator service.

## Contract
A1 Reactor sends:
```json
{
  "prompt": "...",
  "negative_prompt": "...",
  "seed": 1337,
  "fps": 24,
  "seconds": 2.0,
  "width": 768,
  "height": 768,
  "regen_windows": [[0.8, 1.6]]
}
```

Expected response:
```json
{
  "frames": [
    {"index": 0, "png_base64": "..."},
    {"index": 1, "png_base64": "..."}
  ]
}
```

Notes:
- `frames` length must be `ceil(seconds * fps)`
- base64 must be raw PNG bytes (no data URL prefix)

Implementation:
- `src/a1_reactor/providers/http_provider.py`
