#!/usr/bin/env bash
set -euo pipefail

# Demo: open a URL, snapshot, annotated screenshot, then close.
# Usage: ./scripts/agent-browser-demo.sh https://example.com

URL="${1:-https://example.com}"

cd /home/allen6qi/.openclaw/workspace

npx agent-browser open "$URL" > /dev/null

echo "--- SNAPSHOT (truncated) ---"
# Snapshot output can be long; show the first ~120 lines for quick inspection.
npx agent-browser snapshot | sed -n '1,120p'

echo
# Save an annotated screenshot to a deterministic workspace path
OUT="/home/allen6qi/.openclaw/workspace/tmp/agent-browser-annotated.png"
mkdir -p "$(dirname "$OUT")"
npx agent-browser screenshot "$OUT" --annotate > /dev/null

echo "Saved annotated screenshot: $OUT"

npx agent-browser close > /dev/null
