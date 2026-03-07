---
name: daily-idea-candidate-scan
description: Daily scan for app ideas using the “validated apps (1% better)” methodology. Pull candidate projects from X/Twitter (via web search), Product Hunt, and Reddit (r/SideProject + r/AppIdeas). Filter out crypto. Output a Top 10 candidate list with traction/traffic hints and maintenance risk. Write the results into Allen’s Lily Obsidian vault under Brainstorm/Signals/IdeaCandidates/_raw/YYYY-MM-DD.md.
---

# Daily Idea Candidate Scan (Allen)

## Defaults (Allen)
- Audience: mixed (B2B/B2C)
- Exclude categories: **crypto** (hard exclude)
- Time budget: not specified (prefer simple/low-maintenance projects)
- Delivery time: 08:00 Europe/London (handled by cron job)

## Sources (required)
Scan these sources (best-effort):
1) **X/Twitter**: use web search queries for build-in-public + revenue proof (MRR/Stripe).
2) **Product Hunt**: use web search for today/recent Product Hunt launches/trending.
3) **Reddit**: r/SideProject and r/AppIdeas (use web search and/or Reddit JSON listing endpoints).

## Output
Produce **Top 10 candidates**.
For each candidate include:
- Name (or best-guess product name)
- Link
- Source (X / Product Hunt / Reddit)
- What it is (1–2 lines)
- Traction evidence (exact quote if available: MRR/Stripe/users/pricing/testimonials)
- Traffic / acquisition hypothesis (ads / SEO / community / affiliates)
- Maintenance risk (low/med/high + why)
- “1% better” wedge (one concrete angle)

## Filtering rules
- Hard exclude if crypto-related.
- Prefer candidates with:
  - revenue proof (MRR/Stripe) OR clear paid pricing + positive user evidence
  - simple workflow + low ops burden

## Storage (required)
Write a single markdown note to:
- `/mnt/c/Users/allen/Documents/Obsidian/Lily's vault/Brainstorm/Signals/IdeaCandidates/_raw/YYYY-MM-DD.md`

The note format:
- Title: `Idea Candidates — YYYY-MM-DD`
- Then Top 10 numbered list with the fields above.

## Telegram delivery (required)
- After writing the vault note, output the **full Top 10 list** in the same markdown format to the chat (no streaming).
## Implementation guidance
- Use the web_search tool for discovery and then web_fetch for details where useful.
- Keep the note skimmable; avoid long essays.
