---
name: app-idea-generator-reddits
description: Turn Reddit signal lists (problems, pain points, repeated requests) into 10 ranked app ideas with MVP + moat + GTM + validation. Use when Allen asks to generate app ideas from Reddit signals or the daily Top 10 signal report; supports F5Bot-style power flags (include/exclude/group/platform) to steer output.
---

# App Idea Generator (Reddits)

## Inputs
Accept either:
- A pasted list of Reddit “signals” (posts/comments/threads), or
- A pasted daily signal discovery report (Top 10 signals), or
- A short description of the niche + any example threads.

### Optional constraints (best-effort defaults)
If Allen does not specify constraints, assume:
- **Mode:** best-effort (do not block; infer)
- **Audience:** mixed B2B/B2C
- **Platform:** web-first (can include integrations/extensions if it fits)
- **MVP budget:** 7–14 days

If inputs are missing/ambiguous, ask *at most 3* questions, prioritizing:
(a) target user type, (b) B2B vs B2C + pricing preference, (c) MVP time budget.

## Power flags (optional; parsed from user text)
Use these to steer ideation and filtering. If absent, ignore.

- `b2b-only` / `b2c-only`
- `platform=web|ios|android|chrome|cli|slack|discord`
- `mvp<=7days` / `mvp<=14days`
- `group=<name>`: request idea grouping/diversity by category (e.g., devtools, ops, creator, finance)
- `exclude=<term or phrase>` (repeatable)
- `include-any=<term>` (repeatable)
- `include-all=<term>` (repeatable)

Interpretation:
- `exclude=`: avoid ideas whose core workflow depends on that concept.
- `include-any/all=`: prefer ideas whose solution can naturally incorporate those concepts.

## Step 0 — Normalize signals (fast, lightweight)
If signals are raw threads, first create a numbered list:
For each signal, extract best-effort:
- **S#** link (if present), subreddit (if present)
- **Persona** (who is complaining/asking)
- **Pain** (1 sentence)
- **Evidence quote** (1 short snippet from provided text)
- **Workaround** (if mentioned)
- **Frequency**: one-off vs repeated (infer from wording; otherwise unknown)

Keep this normalization brief; then generate ideas.

## Output format (always)
Produce **10 app ideas**, ranked best → worst.

### For each idea (keep compact)
1) **Name (working title)**
2) **Target user**
3) **Problem (1 sentence)**
4) **Proposed solution (2–4 bullets)**
5) **MVP scope (week-1 build)**
6) **Differentiation / moat** (data, workflow lock-in, distribution, integrations, community, etc.)
7) **Risks / unknowns** (pricing, legal, competition, feasibility)
8) **GTM wedge** (where to get first 100 users)
9) **Validation experiment (24–48h)** (specific + cheap + success criteria)
10) **Why this maps to the signals** (cite relevant **S#** and/or links; include at least one short quote)

### Scorecard (for ranking)
Include a one-line score summary per idea:
- **Pain (0–5)**
- **Frequency (0–5)**
- **Buyer clarity (0–5)**
- **MVP feasibility (0–5)**
- **Distribution wedge (0–5)**
- **Moat potential (0–5)**
- **Risk (0–5, higher = worse)**

Rank by overall strength (high positives, low risk). Scores are best-effort.

## Ranking heuristics
Rank higher when:
- Clear pain + urgency + repeated mentions
- Specific persona + workflow
- Obvious distribution path exists (subreddits, SEO queries, integrations, creator channels)
- MVP can be built fast and tested cheaply
- Avoids heavy moderation / high legal risk

## Diversity rules
Avoid 10 near-duplicates.
- Max **2 ideas** per persona/category.
- Aim for **≥4 categories** across the 10 ideas (e.g., devtools, ops, creator tools, personal productivity, finance).

## Evidence rules
- Only cite what the user provided in the signals.
- If there are ≥2 signals, each idea should map to **≥2 signals** when feasible.
- Don’t invent “market facts”; keep claims grounded.

## Style rules
- Be concrete (features, flows, integrations) not vague.
- Prefer “small sharp tool” MVPs over broad platforms.
- Keep each idea compact; don’t write essays.
