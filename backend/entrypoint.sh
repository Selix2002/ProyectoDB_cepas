#!/usr/bin/env bash
set -euo pipefail

# Usamos exec para que los signals (SIGTERM, SIGINT) se propaguen al proceso Litestar
exec litestar run app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --web-concurrency 4
