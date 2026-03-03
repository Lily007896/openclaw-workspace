#!/usr/bin/env bash
set -euo pipefail

# Produce a skimmable Top-10 signal report from today's raw notes.

VAULT_DIR="/mnt/c/Users/allen/Documents/Obsidian/Lily's vault"
DAY="$(date -u +%F)"
RAW_DIR="$VAULT_DIR/Brainstorm/Signals/_raw/$DAY"

if [[ ! -d "$RAW_DIR" ]]; then
  echo "No raw signal folder: $RAW_DIR" >&2
  exit 2
fi

# For now, just list top 10 filenames + links (placeholder).
# The 08:00 cron agent will do the real summarization + top-response fetch.

count=$(ls -1 "$RAW_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
echo "Signals available for $DAY: $count"
