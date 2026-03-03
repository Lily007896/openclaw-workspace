#!/usr/bin/env bash
set -euo pipefail

# Wrapper used by cron
python3 /home/allen6qi/.openclaw/workspace/scripts/collect_reddit_signals.py
