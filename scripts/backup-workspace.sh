#!/usr/bin/env bash
set -euo pipefail

WS_DIR="${OPENCLAW_WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
cd "$WS_DIR"

# Ensure we're on a branch and have a remote.
BRANCH="$(git branch --show-current)"
if [[ -z "${BRANCH}" ]]; then
  echo "Not on a branch (detached HEAD). Aborting." >&2
  exit 2
fi

git remote get-url origin >/dev/null 2>&1 || { echo "Missing git remote 'origin'" >&2; exit 2; }

# Stage changes.
git add -A

# If nothing changed, exit cleanly.
if git diff --cached --quiet; then
  echo "No workspace changes to back up."
  exit 0
fi

STAMP="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
git commit -m "workspace backup ${STAMP}" >/dev/null

git push -u origin "$BRANCH"

echo "Backed up workspace to origin/${BRANCH} (${STAMP})."
