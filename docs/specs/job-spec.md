# Job Spec

JobSpec is the canonical description of what to generate.

Fields:
- prompt
- negative_prompt
- seed
- fps
- seconds
- width/height
- style_preset
- regen_windows (optional)

### JSON example
```json
{
  "prompt": "cinematic shot",
  "seconds": 2.0,
  "fps": 24,
  "seed": 1337,
  "width": 768,
  "height": 768,
  "style_preset": "cinematic",
  "regen_windows": [
    [
      0.8,
      1.6
    ]
  ]
}
```

### Determinism
Keeping prompt + seed stable gives stable results in deterministic providers.
Real model providers may still have nondeterminism depending on runtime.
