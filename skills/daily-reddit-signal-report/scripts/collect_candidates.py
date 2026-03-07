#!/usr/bin/env python3
"""Collect Reddit candidates (posts only) for the daily signal report.

- For each subreddit, fetch up to PER_SUB_LIMIT TOP posts from last day.
- Do NOT fetch comments here (comments are fetched only for the final Top 10).

Outputs JSON to stdout:
{
  "generated_at": 123,
  "window": "day",
  "per_subreddit_limit": 15,
  "subreddits": [...],
  "items": [ { post }, { error }, ... ]
}
"""

import json
import sys
import time
import urllib.parse
import urllib.request

USER_AGENT = "openclaw-daily-signal/1.0"
TIMEOUT_S = 15

SUBREDDITS = [
    "productivity",
    "getdisciplined",
    "selfimprovement",
    "MealPrepSunday",
    "EatCheapAndHealthy",
    "nutrition",
    "loseit",
    "dogs",
    "doggrooming",
    "Dogtraining",
    "puppy101",
    "AppIdeas",
    "SideProject",
]

PER_SUB_LIMIT = 15


def _get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        data = resp.read()
    return json.loads(data.decode("utf-8"))


def fetch_top_posts(subreddit: str, limit: int = PER_SUB_LIMIT):
    url = (
        f"https://www.reddit.com/r/{urllib.parse.quote(subreddit)}/top/.json"
        f"?t=day&limit={int(limit)}"
    )
    j = _get_json(url)
    children = (j.get("data") or {}).get("children") or []
    return [(c.get("data") or {}) for c in children]


def main():
    items = []
    now = int(time.time())

    for sr in SUBREDDITS:
        try:
            posts = fetch_top_posts(sr, PER_SUB_LIMIT)
        except Exception as e:
            items.append({"type": "error", "subreddit": sr, "error": str(e)})
            continue

        for p in posts:
            permalink = p.get("permalink")
            if not permalink:
                continue

            items.append(
                {
                    "type": "post",
                    "subreddit": p.get("subreddit") or sr,
                    "title": p.get("title"),
                    "url": "https://www.reddit.com" + permalink,
                    "permalink": "https://www.reddit.com" + permalink,
                    "author": p.get("author"),
                    "created_utc": p.get("created_utc"),
                    "score": p.get("score"),
                    "num_comments": p.get("num_comments"),
                    "selftext": p.get("selftext") or "",
                    "is_self": p.get("is_self"),
                    "link_flair_text": p.get("link_flair_text"),
                }
            )

    out = {
        "generated_at": now,
        "window": "day",
        "per_subreddit_limit": PER_SUB_LIMIT,
        "subreddits": SUBREDDITS,
        "items": items,
    }

    json.dump(out, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
