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

## Signal sourcing
Reddit-first sourcing rules (subreddits, feed mix, scoring, link hygiene) live in: `memory/topics/signal-sourcing.md`.

## Cron pipeline
- 06:00 `morning-signal-collector` (Reddit-first): collect 8 signals into `Signals/_raw/YYYY-MM-DD/`.
- 08:00 `breathing-session-ideas`: Telegram signal report based on raw signals:
  1) **Top 10 signals**, numbered 1–10.
  2) For each signal include these parts **in this exact order**:
     - **Title** (chosen by Lily)
     - **Summary**: 20–30+ words explaining why it’s a signal and the concrete pain point / what the user wants
     - **Top response (summary)**: ≤30 words
     - **Link**: direct URL to the post
  3) Keep it skimmable; no extra sections.
  4) End with 1 question: which signal to promote today

## Telegram report template (canonical)
Use exactly this structure:

1) **<Title>**
- **Summary:** <20–30+ words; why it’s a signal; concrete pain; what the user wants>
- **Top response (summary):** <≤30 words; if no clear top comment, write “(no clear top comment)”>
- **Link:** <url>

...

10) **<Title>**
- **Summary:** ...
- **Top response (summary):** ...
- **Link:** ...

**Closing question:** Which signal do you want to promote today (pick 1–10)?

## Constraints
- Collector/report may only read/write within `Brainstorm/`.
- Keep everything clean; avoid creating extra folders/notes.
- Avoid Brave rate limits (free plan): keep queries low.

## Backlinking rule (Obsidian)
When Lily creates/updates notes under `Brainstorm/`, add **2–5 intentional backlinks**:
- Signal → link to 1 candidate Problem
- Problem → link to 1–2 People + 1–2 Signals
- Idea → link to exactly 1 Problem (+ optionally 1 Model and 1 API)
Avoid link spam.
