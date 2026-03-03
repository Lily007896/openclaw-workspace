#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
export XDG_CONFIG_HOME="$STATE_DIR/agents/main/qmd/xdg-config"
export XDG_CACHE_HOME="$STATE_DIR/agents/main/qmd/xdg-cache"

qmd update >/dev/null
qmd embed  >/dev/null

echo "qmd-maintain: ok"