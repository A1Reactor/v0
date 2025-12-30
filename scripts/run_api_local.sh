#!/usr/bin/env bash
set -euo pipefail
uvicorn a1_reactor.server.api:app --host 0.0.0.0 --port 8080
