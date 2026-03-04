#!/usr/bin/env bash
set -euo pipefail

# Refresh QMD index + embeddings for all configured collections.
# Use after writing/editing memory files or Obsidian vault notes.

qmd update
qmd embed
