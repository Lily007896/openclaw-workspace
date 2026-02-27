# OpenClaw memory backend: QMD (experimental)

## What it is
OpenClaw can use QMD as a memory backend for hybrid search over markdown files.

## Local setup (WSL2 Ubuntu 24.04)
- Dependencies installed: `sqlite3`, `curl`, `unzip`, build toolchain (`build-essential`, `g++`, `make`, `cmake`)
- Bun installed to `~/.bun/bin`
- QMD installed via bun

## OpenClaw config
In `~/.openclaw/openclaw.json`:
- `memory.backend = "qmd"`
- basic `memory.qmd` defaults enabled

## Models & cache
Models downloaded to `~/.cache/qmd/models` (can be symlinked by OpenClaw).

## GPU status
On WSL2, GPU may not be available; CPU-only mode is fine for small corpora.
