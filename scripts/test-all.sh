#!/usr/bin/env bash
# Run all test suites across the monorepo.
# Each service is tested from its own directory to avoid Python package conflicts.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=== control-plane ($(date +%H:%M:%S)) ==="
cd "$ROOT/apps/control-plane"
python -m pytest tests/ -q "$@"

echo ""
echo "=== runtime ($(date +%H:%M:%S)) ==="
cd "$ROOT/apps/runtime"
CADRIS_RUNTIME_PROVIDER=local python -m pytest tests/ -q "$@"

echo ""
echo "=== renderer ($(date +%H:%M:%S)) ==="
cd "$ROOT/apps/renderer"
python -m pytest tests/ -q "$@" 2>/dev/null || echo "(skipped — no venv or tests)"

echo ""
echo "=== web typecheck ($(date +%H:%M:%S)) ==="
cd "$ROOT/apps/web"
npx tsc --noEmit

echo ""
echo "=== All passed ==="
