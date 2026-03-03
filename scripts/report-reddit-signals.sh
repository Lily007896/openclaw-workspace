#!/usr/bin/env bash
set -euo pipefail

VAULT_DIR="/mnt/c/Users/allen/Documents/Obsidian/Lily's vault"
DAY="$(date -u +%F)"
RAW_DIR="$VAULT_DIR/Brainstorm/Signals/_raw/$DAY"

if [[ ! -d "$RAW_DIR" ]]; then
  echo "No raw signals folder: $RAW_DIR" >&2
  exit 2
fi

mapfile -t files < <(ls -1t "$RAW_DIR"/reddit-*.md 2>/dev/null | head -n 10)

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No reddit signal files found in: $RAW_DIR" >&2
  exit 2
fi

echo "Top 10 signals ($DAY)"
echo

extract_first_after_heading() {
  local file="$1" heading="$2"
  awk -v h="$heading" 'BEGIN{p=0} $0==h{p=1;next} /^## /{if(p==1)exit} {if(p==1 && $0!="") {print; exit}}' "$file" | sed 's/^- *//'
}

for f in "${files[@]}"; do
  title=$(sed -n '1s/^# *//p' "$f" | head -n 1)
  link=$(grep -m1 "^- Link:" "$f" | sed 's/^- Link: *//')
  why=$(extract_first_after_heading "$f" "## Why it matters")
  top=$(extract_first_after_heading "$f" "## Top response (<=30 words)")

  echo "- ${title}"
  echo "  Link: ${link}"
  echo "  Why: ${why}"
  echo "  Top response: ${top}"
  echo

done

echo "Question: which signal should we promote today? Reply with the number 1-10."
