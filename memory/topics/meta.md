# Meta (topic memory)

Rules about how Lily should operate (memory hygiene, reporting formats, housekeeping).

## Memory hygiene
- When recording a new pattern/setup, check for conflicts/outdated info.
- Update the canonical topic memory (`memory/topics/<topic>.md`) so it stays correct.
- Daily journal (`memory/YYYY-MM-DD.md`) should record only the delta/decision made that day.
- Keep `MEMORY.md` clean: index + high-signal preferences, link out to topic files.
- **After writing/editing** any memory/knowledge notes (either in `~/.openclaw/workspace/` or the Obsidian vault), run QMD refresh so `memory_search` stays accurate:
  - `scripts/qmd-refresh.sh` (runs `qmd update` + `qmd embed`)

## Reporting hygiene
- Prefer skimmable outputs with links to details.
- Brainstorm 08:00 signal report format is defined in `memory/topics/brainstorm.md`.

## Backlink hygiene (Obsidian)
- Add a few intentional links; avoid turning notes into link dumps.
- Prefer 2–5 links that explain relationships.

## Voice mode toggle
- If Allen says **"voice on"**, reply using English TTS by default until Allen says **"voice off"**.
- Persist toggle state in `workspace/state/voice-mode.json`.

## News lookup preference
- On-demand only (no scheduled news tasks).
- Preferred sources: Reuters first. UK sources as needed: BBC, ITV, Sky.
- Skip paywalled sources.
- Output: concise bullets + links; separate confirmed vs unclear.

## Browser automation preference
- When a browser is needed, prefer using Vercel Labs **agent-browser**: https://github.com/vercel-labs/agent-browser
- Fall back to OpenClaw `browser` tool only when agent-browser is not suitable/available.
