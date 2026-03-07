---
name: daily-reddit-signal-report
description: Generate Allen's daily Top 10 Reddit signal report (last 24h) from a fixed subreddit set. Strict keyword matching (no synonyms), exclude crypto/politics, fetch up to 15 TOP(24h) posts per subreddit, fetch top 1 non-AutoMod comment only for the final Top 10, and bias toward productivity (~7/10). Use when Allen asks for the daily signal report or when a cron job should run the daily report.
---

# Daily Reddit Signal Report (Allen)

## Goal
Produce a **Top 10** “signal report” from Reddit (last 24h) that surfaces actionable pain points and requests.

## Fixed configuration (defaults)
### Sources
- Reddit only
- Window: **TOP(24h)**

### Subreddits
Scan these subreddits:
- r/productivity
- r/getdisciplined
- r/selfimprovement
- r/MealPrepSunday
- r/EatCheapAndHealthy
- r/nutrition
- r/loseit
- r/dogs
- r/doggrooming
- r/Dogtraining
- r/puppy101
- r/AppIdeas
- r/SideProject

### Fetch limits
- Per subreddit: fetch up to **15** posts from **TOP(24h)** only (no NEW)
- Comments: fetch comments **only for the final Top 10**. For each included signal, fetch **top 1 comment** that is **not** AutoMod/sticky/mod-bot.

### Keywords (strict labels)
Allowed matched keyword labels (strict):
- productivity
- health
- dogs
- dog grooming
- idea generation
- meal prep

Strict matching rule:
- The **Matched keywords** field must be a subset of the labels above.
- Do **not** invent synonyms (e.g., “planning”, “prioritization”).

Label matching logic (best-effort but strict labels):
- productivity: literal contains "productivity"
- health: literal contains "health"
- dogs: contains "dog" or "dogs"
- dog grooming: contains ("groom" or "grooming") AND ("dog" or "dogs")
- meal prep: contains "meal prep" or "mealprep"
- idea generation: contains "idea generation" OR (contains "idea" AND contains "generate")

### Exclusions
Hard exclude if title/body contains:
- crypto
- politics

## Workflow
1) **Collect candidates (posts only)** using the bundled script:
   - Run: `python3 scripts/collect_candidates.py`
   - It outputs JSON to stdout (candidate list with post fields; **no comments fetched here**).

2) **Filter** candidates:
   - Drop anything that hits exclusions.
   - Compute Matched keywords using the strict rules above.
   - Drop any candidate with zero matched keywords.

3) **Rank + select Top 10**
   - Strongly prefer **productivity**.
   - Target composition: ~**7/10** signals where Matched keywords includes **productivity**.
   - Remaining up to 3 can be other topics only if unusually strong (pain + buildability).

4) **Fetch top comments for the final Top 10**
   - Run: `python3 scripts/fetch_top_comments.py` with a JSON list of selected post permalinks/URLs.
   - Attach the returned top-comment (non-AutoMod/sticky/mod-bot) to each final signal.

5) **Write the report** in the required format (below).

## Output format (required)
For each signal (1–10), output:
- **Title (subreddit) + Link**
- **Persona + pain point** (immediately under title)
- **1–2 line summary**
- **Evidence quote snippet** (short quote from OP content)
- **Matched keywords** (only from the strict label list)
- **Top reply summary** (from top 1 non-AutoMod comment)
- **Score**: pain, urgency, frequency, buildability (0–5 each)

## Persona + pain point quality rules
- Must be **specific to that thread** (no generic “dog owner wants calmer routine”).
- Avoid repeating the same persona phrase across multiple signals.
- Keep to **one concise line**.

## Token/cost minimization
- Prefer short quotes/snippets.
- Do not fetch more than the specified limits.
- Avoid fetching comments for non-final candidates (fetch comments only after Top 10 selection).

