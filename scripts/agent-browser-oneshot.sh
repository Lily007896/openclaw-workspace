#!/usr/bin/env bash
set -euo pipefail

# One-shot helper: open URL -> snapshot -> (optional) annotated screenshot -> close
# Usage:
#   ./scripts/agent-browser-oneshot.sh <url> [--screenshot]
#
# Output:
#   - prints snapshot to stdout
#   - if --screenshot, saves annotated screenshot to workspace/tmp/

URL="${1:-}"
FLAG="${2:-}"

if [[ -z "$URL" ]]; then
  echo "Usage: $0 <url> [--screenshot]" >&2
  exit 2
fi

cd /home/allen6qi/.openclaw/workspace

./scripts/agent-browser.sh open "$URL" > /dev/null

# snapshot can be long; caller can pipe to head/sed/etc.
./scripts/agent-browser.sh snapshot

if [[ "$FLAG" == "--screenshot" ]]; then
  OUT="/home/allen6qi/.openclaw/workspace/tmp/agent-browser-annotated-$(date -u +%Y%m%dT%H%M%SZ).png"
  mkdir -p "$(dirname "$OUT")"
  ./scripts/agent-browser.sh screenshot "$OUT" --annotate > /dev/null
  echo "Saved annotated screenshot: $OUT" >&2
fi

./scripts/agent-browser.sh close > /dev/null
