#!/usr/bin/env bash
# Generate TypeScript types from the control-plane OpenAPI schema.
#
# Usage:
#   ./scripts/generate-schemas.sh           # control-plane must be running on :8000
#   ./scripts/generate-schemas.sh <url>     # custom OpenAPI URL
#
# Output: packages/schemas/src/generated.ts
# The hand-written index.ts re-exports and extends these generated types
# with frontend-only additions (SSE event types, label maps, etc.)

set -euo pipefail

OPENAPI_URL="${1:-http://localhost:8000/openapi.json}"
OUT_DIR="$(cd "$(dirname "$0")/.." && pwd)/packages/schemas/src"

echo "Fetching OpenAPI schema from $OPENAPI_URL ..."
npx openapi-typescript "$OPENAPI_URL" -o "$OUT_DIR/generated.ts"

echo "Generated: $OUT_DIR/generated.ts"
echo ""
echo "Tip: compare with index.ts to find drift:"
echo "  diff <(grep 'export interface' $OUT_DIR/generated.ts | sort) \\"
echo "       <(grep 'export interface' $OUT_DIR/index.ts | sort)"
