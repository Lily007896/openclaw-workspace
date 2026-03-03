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

# Reddit endpoints (no auth). Keep it small to avoid rate limits.
SUBREDDITS = [
    "ProductivityApps",
    "macapps",
    "MealPrepSunday",
    "beginnerfitness",
    "AI_Agents",
    "AiAutomations",
]
POSTS_PER_SUB = 2
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

    # 1-line why: derived from title/snippet
    why = snippet.strip() or "Active request/discussion that may contain pain signals."
    why = re.sub(r"\s+", " ", why)
    if len(why) > 140:
        why = why[:140] + "…"

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


def main():
    wrote = 0
    for si, sub in enumerate(SUBREDDITS):
        if si:
            time.sleep(1.2)
        url = f"https://www.reddit.com/r/{sub}/new.json?limit=10"
        try:
            data = fetch_json(url)
        except Exception:
            continue
        posts = (data.get("data") or {}).get("children") or []
        picked = 0
        for p in posts:
            if picked >= POSTS_PER_SUB:
                break
            d = p.get("data") or {}
            title = (d.get("title") or "").strip()
            permalink = d.get("permalink") or ""
            post_url = "https://www.reddit.com" + permalink
            snippet = (d.get("selftext") or "").strip()
            if not snippet:
                snippet = (d.get("url") or "").strip()
            snippet = re.sub(r"\s+", " ", snippet)
            if len(snippet) > 180:
                snippet = snippet[:180] + "…"
            if not title or not permalink:
                continue
            write_note(title, post_url, snippet, permalink)
            wrote += 1
            picked += 1
            time.sleep(0.8)

    print(f"Wrote files to: {OUT_DIR}")
    print(f"count={len(list(OUT_DIR.glob('reddit-*.md')))}")


if __name__ == "__main__":
    main()
