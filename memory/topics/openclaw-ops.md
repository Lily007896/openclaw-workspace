# OpenClaw ops (topic memory)

Technical notes about running/operating OpenClaw on this machine.

## Cron + filesystem constraints
- OpenClaw cron “agent turns” may be restricted by workspace-root file tooling.
- The built-in write tool can fail when writing to paths outside the workspace root (e.g., Obsidian vault under `/mnt/c/...`), with errors like: `Path escapes workspace root`.
- For scheduled collectors/reports that must write into the Obsidian vault, use **workspace-resident scripts** (shell/python3 doing normal filesystem operations) to write to vault paths.

## Cron reliability guidelines
- Keep cron jobs lightweight to avoid timeouts.
- Prefer two-stage pipelines: collect data → save files → generate report from files.
- Avoid relying on `python`; use `python3` explicitly.

## Signal pipeline incident (2026-03-03)
- Root cause: 06:00 collector attempted to use OpenClaw write tool to `/mnt/c/...` and failed.
- Fix: move collector + reporter into scripts under `~/.openclaw/workspace/scripts/`.

## QMD retrieval incident (2026-03-03)
- Symptom: `memory_search` returned empty results even for known strings.
- Root cause: QMD had a large embedding backlog (indexed files without vectors), so semantic retrieval was ineffective.
- Fix: ran `qmd update` + `qmd embed`, then scheduled hourly maintenance via cron `qmd-hourly-embed` running `scripts/qmd-maintain.sh`.
- Runbook: when retrieval seems broken, check `qmd status` for pending embeddings.

## Voice toggle implementation
- State file: `~/.openclaw/workspace/state/voice-mode.json`
- Purpose: let Allen switch between text and TTS without prefixing every message.
