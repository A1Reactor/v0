# Overview

A1 Reactor is a **pipeline** and **interfaces** project.

It deliberately separates:
- *Orchestration* (job specs, caching, stitching)
- *Model provider* (local/hosted/mock)
- *Evaluation* (basic metrics, diffs)
- *Transport* (HTTP API)

If you want to plug in a real model backend, start here:
- `docs/providers/`
- `src/a1_reactor/providers/`

