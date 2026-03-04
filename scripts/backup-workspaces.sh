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

# 1) Sync Windows Obsidian vault into Lily workspace for Git backup
LILY_DIR="${OPENCLAW_WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
WIN_VAULT="/mnt/c/Users/allen/Documents/Obsidian/Lily's vault"
WS_VAULT="$LILY_DIR/obsidian-vault"
mkdir -p "$WS_VAULT"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete --exclude '.obsidian/' --exclude '.trash/' "$WIN_VAULT/" "$WS_VAULT/"
else
  rm -rf "$WS_VAULT"/*
  cp -a "$WIN_VAULT/." "$WS_VAULT/"
fi

# 2) Backup Lily + Moss
backup_repo "$LILY_DIR" "workspace" 
backup_repo "$HOME/.openclaw/workspace-work" "moss-memory"
