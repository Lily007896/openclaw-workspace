#!/usr/bin/env python3
"""Fetch the top 1 non-AutoMod/sticky/mod-bot comment for each selected Reddit post.

Input: JSON on stdin, either:
- a list of objects with {"permalink": "https://www.reddit.com/r/..."} or {"url": "..."}
- a list of strings (URLs/permalinks)

Output: JSON list aligned to input order:
[{"top_comment": {author, score, body, permalink} | null, "error": str|None}, ...]
"""

import json
import sys
import urllib.request

USER_AGENT = "openclaw-daily-signal/1.0"
TIMEOUT_S = 15


def _get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        data = resp.read()
    return json.loads(data.decode("utf-8"))


def _normalize_permalink(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        return x.get("permalink") or x.get("url")
    return None


def pick_top_comment(post_permalink_url: str):
    # Expect a full reddit URL to the post, e.g. https://www.reddit.com/r/.../comments/.../
    # Comments JSON endpoint is the same URL with .json
    if not post_permalink_url:
        return None

    url = post_permalink_url
    if url.endswith("/"):
        url = url[:-1]
    url = url + ".json?limit=12"

    j = _get_json(url)
    if not isinstance(j, list) or len(j) < 2:
        return None

    comments_listing = j[1]
    children = ((comments_listing.get("data") or {}).get("children")) or []

    for c in children:
        if c.get("kind") != "t1":
            continue
        d = c.get("data") or {}
        author = (d.get("author") or "")
        author_l = author.lower()
        body = d.get("body") or ""

        stickied = bool(d.get("stickied"))
        distinguished = (d.get("distinguished") or "")

        if stickied:
            continue
        if not body.strip():
            continue
        if author_l in ("automoderator", "reddit"):
            continue
        if "bot" in author_l:
            continue
        if distinguished in ("moderator", "admin"):
            continue

        return {
            "author": author,
            "score": d.get("score"),
            "body": body,
            "permalink": "https://www.reddit.com" + (d.get("permalink") or ""),
        }

    return None


def main():
    inp = json.load(sys.stdin)
    if not isinstance(inp, list):
        raise SystemExit("Input must be a JSON list")

    out = []
    for item in inp:
        try:
            perma = _normalize_permalink(item)
            tc = pick_top_comment(perma)
            out.append({"top_comment": tc, "error": None})
        except Exception as e:
            out.append({"top_comment": None, "error": str(e)})

    json.dump(out, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
