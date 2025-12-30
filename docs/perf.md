# Performance notes

A1 Reactor tries to keep the pipeline predictable.

## Hot paths
- frame encode/decode
- stitching (ffmpeg)
- provider calls (network or model runtime)

## Recommendations
- keep frames on SSD
- avoid re-encoding if you only regen a small window
- cache provider responses if you iterate with same seed/prompt
