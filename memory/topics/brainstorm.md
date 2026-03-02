# Brainstorm (topic memory)

## Goal
Build a product people use that generates income (solo developer, AI-assisted).

## Obsidian structure (vault)
- `Brainstorm/Signals/_raw/YYYY-MM-DD/` — raw daily signals (short notes)
- `Brainstorm/Problems/` — promoted, cleaned-up problem statements
- `Brainstorm/Ideas/` — candidate solutions linked to Problems
- `Brainstorm/Experiments/` — validation experiments
- `Brainstorm/People/` — personas
- `Brainstorm/Models/` — business model templates (knowledge base)
- `Brainstorm/APIs/` — API catalog (knowledge base)

## Workflow definitions
- **Signal**: disposable input (link + snippet + 2-line why-it-matters + tags).
- **Promote**: upgrade a Signal → Problem (and optionally → Idea) when it’s worth investing in.

## Cron pipeline
- 06:00 `morning-signal-collector` (Reddit-first): collect 8 signals into `Signals/_raw/YYYY-MM-DD/`.
- 08:00 `breathing-session-ideas`: Telegram signal report based on raw signals:
  1) **Top 10 signals**
     - Each signal includes: Title, Link, 1-line “Why it matters”, and fetched “Top response” summary (≤30 words)
  2) End with 1 question: which signal to promote today

## Constraints
- Collector/report may only read/write within `Brainstorm/`.
- Keep everything clean; avoid creating extra folders/notes.
- Avoid Brave rate limits (free plan): keep queries low.
