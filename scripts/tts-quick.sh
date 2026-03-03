#!/usr/bin/env bash
set -euo pipefail

# Quick TTS helper for short messages (keeps latency down).
# Usage: echo "text" | ./tts-quick.sh

text=$(cat)
text=${text:0:900}

python3 - <<'PY' "$text"
import sys
from openclaw.tools.tts import tts
# Note: This is a placeholder; OpenClaw TTS is normally invoked by the agent runtime.
print(sys.argv[1])
PY