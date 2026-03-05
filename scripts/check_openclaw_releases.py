#!/usr/bin/env python3
"""Check GitHub Releases for openclaw/openclaw and write impact-focused daily notes.

- Writes to: <Vault>/Clawbot/OpenClaw Updates/Daily/YYYY-MM-DD.md
- Keeps state in: ~/.openclaw/workspace/state/openclaw-releases.json
- Skips writing anything if no new releases since last seen.

Heuristics:
- Ignore routine bug-fix bullets.
- Keep: new features, breaking changes, deprecations, config/ops changes, security, migrations.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO = "openclaw/openclaw"
API_URL = f"https://api.github.com/repos/{REPO}/releases?per_page=10"

VAULT_DIR = Path("/mnt/c/Users/allen/Documents/Obsidian/Lily's vault")
OUT_DIR = VAULT_DIR / "Clawbot" / "OpenClaw Updates" / "Daily"
STATE_PATH = Path(os.environ.get("OPENCLAW_WORKSPACE_DIR", str(Path.home() / ".openclaw" / "workspace"))) / "state" / "openclaw-releases.json"

IMPORTANT_KEYWORDS = [
    "breaking",
    "deprecat",
    "migration",
    "upgrade",
    "config",
    "gateway",
    "cron",
    "scheduler",
    "auth",
    "token",
    "permission",
    "security",
    "vulnerability",
    "model",
    "tool",
    "api",
    "protocol",
    "database",
    "storage",
]

BUGFIX_ONLY_PAT = re.compile(r"\b(fix|fixed|fixes|bug|typo|minor|cleanup|refactor|lint)\b", re.I)
FEATURE_PAT = re.compile(r"\b(add|added|new|introduc|support|enable|feature)\b", re.I)


def _http_json(url: str):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "openclaw-update-check/1.0",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _load_state() -> dict:
    try:
        return json.loads(STATE_PATH.read_text("utf-8"))
    except FileNotFoundError:
        return {"last_seen_tag": None}
    except Exception:
        return {"last_seen_tag": None}


def _save_state(tag: str | None):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps({"last_seen_tag": tag}, indent=2) + "\n", "utf-8")


def _looks_important(line: str) -> bool:
    s = line.strip().lower()
    if not s:
        return False
    if any(k in s for k in IMPORTANT_KEYWORDS):
        return True
    if FEATURE_PAT.search(s):
        return True
    # keep security even if phrased like a fix
    if "security" in s:
        return True
    return False


def _filter_body(md: str) -> list[str]:
    """Return important bullets/lines from release notes body."""
    lines = [l.rstrip() for l in md.splitlines()]
    out: list[str] = []

    for l in lines:
        s = l.strip()
        if not s:
            continue

        # Keep headings if they signal importance
        if s.startswith("#"):
            if _looks_important(s):
                out.append(s)
            continue

        is_bullet = s.startswith(('-', '*')) or re.match(r"^\d+\.", s)
        if is_bullet:
            # drop pure bugfix bullets unless they look important
            if BUGFIX_ONLY_PAT.search(s) and not _looks_important(s):
                continue
            if _looks_important(s) or not BUGFIX_ONLY_PAT.search(s):
                out.append(s)
        else:
            # keep short impactful lines that look like changes
            if _looks_important(s) and len(s) <= 200:
                out.append(s)

    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for l in out:
        key = l.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(l)

    return deduped[:40]


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    state = _load_state()
    last_seen = state.get("last_seen_tag")

    releases = _http_json(API_URL)
    if not isinstance(releases, list) or not releases:
        print("No releases found (API returned empty).")
        return 0

    # GitHub returns newest first
    new_releases = []
    for r in releases:
        tag = r.get("tag_name")
        if not tag:
            continue
        if last_seen and tag == last_seen:
            break
        # skip drafts/prereleases
        if r.get("draft") or r.get("prerelease"):
            continue
        new_releases.append(r)

    if not new_releases:
        # Intentionally print nothing so the cron job can stay silent.
        return 0

    today = dt.datetime.now(dt.timezone.utc).astimezone().date().isoformat()
    note_path = OUT_DIR / f"{today}.md"

    blocks = []
    blocks.append(f"# OpenClaw Updates — {today}\n")
    blocks.append(f"Source: https://github.com/{REPO}/releases\n")

    # Oldest first for readability
    for r in reversed(new_releases):
        name = (r.get("name") or r.get("tag_name") or "(untitled)").strip()
        tag = (r.get("tag_name") or "").strip()
        url = (r.get("html_url") or "").strip()
        pub = (r.get("published_at") or "").strip()
        body = r.get("body") or ""

        important = _filter_body(body)

        blocks.append("---\n")
        blocks.append(f"## {name}\n")
        blocks.append(f"- Tag: `{tag}`\n")
        if pub:
            blocks.append(f"- Published: {pub}\n")
        if url:
            blocks.append(f"- Link: {url}\n")

        if important:
            blocks.append("\n### Impact-relevant notes (filtered)\n")
            for l in important:
                blocks.append(f"{l}\n")
        else:
            blocks.append("\n### Impact-relevant notes (filtered)\n")
            blocks.append("(No obvious impact-relevant items found; release appears mostly bug-fix / maintenance.)\n")

    note_path.write_text("".join(blocks), "utf-8")

    # update last seen to newest tag (even if multiple)
    newest_tag = next((r.get("tag_name") for r in releases if r.get("tag_name")), None)
    _save_state(newest_tag)

    # Print a short message that a cron agent can forward to Telegram.
    newest_names = [((r.get("name") or r.get("tag_name") or "").strip()) for r in new_releases]
    newest_names = [n for n in newest_names if n]
    latest_release = new_releases[0]
    latest_title = (latest_release.get("name") or latest_release.get("tag_name") or "").strip()
    latest_url = (latest_release.get("html_url") or "").strip()

    # Pull a few impact lines from the latest release only for the chat message
    latest_important = _filter_body(latest_release.get("body") or "")
    latest_important = [l for l in latest_important if l.strip()][:8]

    msg_lines = []
    msg_lines.append(f"OpenClaw release update: {len(new_releases)} new release(s) detected")
    if latest_title:
        msg_lines.append(f"Latest: {latest_title}")
    if latest_url:
        msg_lines.append(f"{latest_url}")
    if latest_important:
        msg_lines.append("\nImpact-relevant highlights (bug-fix-only items skipped):")
        for l in latest_important[:6]:
            msg_lines.append(f"- {l.lstrip('-* ').strip()}")
    msg_lines.append(f"\nVault note: {note_path}")

    print("\n".join(msg_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
