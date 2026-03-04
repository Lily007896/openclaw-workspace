#!/usr/bin/env python3
import datetime, hashlib, json, os, re, sys, time, urllib.request
from pathlib import Path

VAULT_DIR = Path("/mnt/c/Users/allen/Documents/Obsidian/Lily's vault")
DAY = datetime.date.today().isoformat()
OUT_DIR = VAULT_DIR / "Brainstorm" / "Signals" / "_raw" / DAY
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Clean previous reddit files for the day (avoid stale placeholders)
for f in OUT_DIR.glob('reddit-*.md'):
    try:
        f.unlink()
    except Exception:
        pass

# Reddit endpoints (no auth). Broad productivity scan.
# Strategy: pull more candidates across 18 subs, then score/filter down to Top 10.
SUBREDDITS = [
    # Broad productivity
    "productivity",
    "ProductivityApps",
    "GetDisciplined",
    "selfimprovement",
    "lifehacks",
    "DecidingToBeBetter",
    # Tools / notes
    "todoist",
    "ticktick",
    "ThingsApp",
    "Notion",
    "ObsidianMD",
    "NoteTaking",
    # Habits / routines
    "habits",
    "TimeManagement",
    "studytips",
    # ADHD (included)
    "ADHD",
    "ADHDWomen",
    "AuDHDWomen",
]

# Candidate collection parameters
TOP_WEEK_PER_SUB = 2
NEW_PER_SUB = 1
NEW_SUBS = {"ProductivityApps", "ADHD", "ADHDWomen", "AuDHDWomen", "ObsidianMD"}

WORD_LIMIT = 30

UA = "Mozilla/5.0 (compatible; OpenClawSignalCollector/1.0)"


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8", "ignore"))


def top_comment_summary(permalink: str) -> str:
    url = "https://www.reddit.com" + permalink
    if not url.endswith("/"):
        url += "/"
    url += ".json?sort=top&limit=2"
    try:
        data = fetch_json(url)
        children = data[1]["data"].get("children", [])
        for c in children:
            if c.get("kind") == "t1":
                body = c["data"].get("body", "")
                if body and body not in ("[deleted]", "[removed]"):
                    body = re.sub(r"\s+", " ", body).strip()
                    return " ".join(body.split(" ")[:WORD_LIMIT])
    except Exception:
        pass
    return "(no clear top comment)"


def write_note(title: str, url: str, snippet: str, permalink: str):
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    path = OUT_DIR / f"reddit-{h}.md"

    # Why (20–30 words): make it understandable without clicking.
    base = re.sub(r"\s+", " ", (snippet or "").strip())
    if not base:
        base = title
    # Build a short, explicit interpretation and cap to ~30 words.
    why_text = f"Signal about user demand/pain: {base}"
    words = why_text.split()
    # Ensure at least ~20 words by appending a generic tail if too short.
    if len(words) < 20:
        words += "This indicates a concrete workflow gap and a user actively looking for a better tool or solution".split()
    why = " ".join(words[:30])

    top = top_comment_summary(permalink)

    content = (
        f"# Signal: {title}\n\n"
        f"- Platform: Reddit\n"
        f"- Link: {url}\n"
        f"- Snippet: {snippet}\n\n"
        f"## Why it matters\n"
        f"- {why}\n\n"
        f"## Top response (<=30 words)\n"
        f"- {top}\n"
    )
    path.write_text(content, encoding="utf-8")


def score_candidate(title: str, snippet: str) -> int:
    """Simple heuristic score for "signal quality"."""
    t = (title + " " + snippet).lower()
    score = 0
    # High-intent / tool-seeking patterns
    pats = [
        "looking for", "is there", "any app", "any tool", "alternative", "alternatives",
        "recommend", "what do you use", "how do you", "help me choose", "workflow",
        "tried", "doesn't work", "overwhelmed", "too many", "friction", "habit",
        "calendar", "planner", "todo", "task", "reminder", "routine",
    ]
    for p in pats:
        if p in t:
            score += 2
    # Questions tend to be better signals
    if "?" in title:
        score += 2
    # Longer snippet sometimes means more detail/requirements
    score += min(len(snippet) // 60, 4)
    return score


def extract_post(d: dict, expected_sub: str | None = None):
    title = (d.get("title") or "").strip()
    permalink = d.get("permalink") or ""
    actual_sub = (d.get("subreddit") or "").strip()
    if expected_sub and actual_sub and actual_sub.lower() != expected_sub.lower():
        # Guard against rare cross-subreddit mismatches.
        return None
    if not title or not permalink:
        return None
    # Use Reddit's canonical permalink (includes correct subreddit path)
    url = "https://www.reddit.com" + permalink
    snippet = (d.get("selftext") or "").strip()
    if not snippet:
        snippet = (d.get("url") or "").strip()
    snippet = re.sub(r"\s+", " ", snippet)
    if len(snippet) > 180:
        snippet = snippet[:180] + "…"
    return title, url, snippet, permalink


def main():
    candidates = []

    for si, sub in enumerate(SUBREDDITS):
        if si:
            time.sleep(1.0)

        # 1) Quality: top posts in the past week
        try:
            data = fetch_json(f"https://www.reddit.com/r/{sub}/top.json?t=week&limit=20")
            posts = (data.get("data") or {}).get("children") or []
            taken = 0
            for p in posts:
                if taken >= TOP_WEEK_PER_SUB:
                    break
                ex = extract_post(p.get("data") or {}, expected_sub=sub)
                if not ex:
                    continue
                title, url, snippet, permalink = ex
                candidates.append((score_candidate(title, snippet), sub, title, url, snippet, permalink))
                taken += 1
        except Exception:
            pass

        # 2) Freshness: newest posts (only for selected subs)
        if sub in NEW_SUBS:
            try:
                time.sleep(0.6)
                data = fetch_json(f"https://www.reddit.com/r/{sub}/new.json?limit=15")
                posts = (data.get("data") or {}).get("children") or []
                taken = 0
                for p in posts:
                    if taken >= NEW_PER_SUB:
                        break
                    ex = extract_post(p.get("data") or {}, expected_sub=sub)
                    if not ex:
                        continue
                    title, url, snippet, permalink = ex
                    candidates.append((score_candidate(title, snippet), sub, title, url, snippet, permalink))
                    taken += 1
            except Exception:
                pass

    # Dedupe by URL, keep best score
    best = {}
    for sc, expected_sub, title, url, snippet, permalink in candidates:
        if url not in best or sc > best[url][0]:
            best[url] = (sc, expected_sub, title, snippet, permalink)

    ranked = sorted(
        [(sc, url, expected_sub, title, snippet, permalink)
         for url, (sc, expected_sub, title, snippet, permalink) in best.items()],
        reverse=True,
    )

    def verify_subreddit(permalink: str, expected_sub: str) -> bool:
        # Fetch the post JSON and confirm subreddit matches.
        url = "https://www.reddit.com" + (permalink if permalink.endswith('/') else permalink + '/') + ".json?limit=1"
        try:
            data = fetch_json(url)
            post = data[0]['data']['children'][0]['data']
            actual = (post.get('subreddit') or '').strip()
            return actual.lower() == expected_sub.lower()
        except Exception:
            return False

    wrote = 0
    for sc, url, expected_sub, title, snippet, permalink in ranked:
        if wrote >= 10:
            break
        if not verify_subreddit(permalink, expected_sub):
            continue
        # Use subreddit-free canonical link to avoid client redirect confusion
        post_id = permalink.strip('/').split('/')[-2] if '/comments/' in permalink else ''
        final_url = f"https://www.reddit.com/comments/{post_id}/" if post_id else url
        write_note(title, final_url, snippet, permalink)
        wrote += 1
        time.sleep(0.8)

    if wrote < 10:
        print(f"Warning: only wrote {wrote} verified signals", file=sys.stderr)

    print(f"Wrote files to: {OUT_DIR}")
    print(f"count={len(list(OUT_DIR.glob('reddit-*.md')))}")


if __name__ == "__main__":
    main()
