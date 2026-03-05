#!/usr/bin/env bash
set -euo pipefail

# Backup BOTH Lily + Moss workspaces.
# - Lily workspace repo: ~/.openclaw/workspace (existing)
# - Moss workspace repo: ~/.openclaw/workspace-work (new)
#
# This script commits + pushes changes if any.

backup_repo() {
  local dir="$1"
  local label="$2"

  if [[ ! -d "$dir" ]]; then
    echo "[$label] Missing dir: $dir" >&2
    return 2
  fi

  pushd "$dir" >/dev/null

  # Ensure we're on a branch and have a remote.
  local branch
  branch="$(git branch --show-current)"
  if [[ -z "$branch" ]]; then
    echo "[$label] Not on a branch (detached HEAD)." >&2
    popd >/dev/null
    return 2
  fi

  git remote get-url origin >/dev/null 2>&1 || { echo "[$label] Missing git remote 'origin'" >&2; popd >/dev/null; return 2; }

  git add -A

  if git diff --cached --quiet; then
    echo "[$label] No changes." 
    popd >/dev/null
    return 0
  fi

  local stamp
  stamp="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
  git commit -m "${label} backup ${stamp}" >/dev/null || true
  git push -u origin "$branch" >/dev/null

  echo "[$label] Backed up to origin/${branch} (${stamp})."
  popd >/dev/null
}

# Backup Lily + Moss (workspace repos only)
LILY_DIR="${OPENCLAW_WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
backup_repo "$LILY_DIR" "workspace"
backup_repo "$HOME/.openclaw/workspace-work" "moss-memory"
