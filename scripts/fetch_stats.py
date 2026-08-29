#!/usr/bin/env python3
"""
fetch_stats.py
──────────────
Fetches GitHub stats from the public REST API:
  • profile: public repos, followers, following
  • stars received across owned repos
  • totals via the search API: commits, PRs, merged PRs, issues

Uses GITHUB_TOKEN / GH_TOKEN if set (recommended in Actions) but works
unauthenticated too. On any per-field failure, the previous value from
data/stats.json is kept so a rate-limited run never zeroes things out.

Output: data/stats.json
"""

import json
import os
import pathlib

import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "stats.json"
USERNAME = "arnavsao"

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": f"{USERNAME}-profile-stats",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def get_json(url: str, params: dict | None = None):
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def search_count(endpoint: str, query: str) -> int:
    data = get_json(f"{API}/search/{endpoint}", {"q": query, "per_page": 1})
    return int(data["total_count"])


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    # start from previous values so partial failures don't zero fields
    stats: dict = {}
    if OUTPUT.exists():
        try:
            stats = json.loads(OUTPUT.read_text())
        except Exception:
            stats = {}

    try:
        user = get_json(f"{API}/users/{USERNAME}")
        stats["repositories"] = user.get("public_repos", stats.get("repositories", 0))
        stats["followers"] = user.get("followers", stats.get("followers", 0))
        stats["following"] = user.get("following", stats.get("following", 0))
    except Exception as e:
        print(f"Warning: profile fetch failed: {e}")

    try:
        stars = 0
        page = 1
        while True:
            repos = get_json(f"{API}/users/{USERNAME}/repos",
                             {"per_page": 100, "page": page, "type": "owner"})
            stars += sum(r.get("stargazers_count", 0) for r in repos)
            if len(repos) < 100:
                break
            page += 1
        stats["stars"] = stars
    except Exception as e:
        print(f"Warning: stars fetch failed: {e}")

    for key, endpoint, query in [
        ("commits",    "commits", f"author:{USERNAME}"),
        ("prs",        "issues",  f"author:{USERNAME} type:pr"),
        ("prs_merged", "issues",  f"author:{USERNAME} type:pr is:merged"),
        ("issues",     "issues",  f"author:{USERNAME} type:issue"),
    ]:
        try:
            stats[key] = search_count(endpoint, query)
        except Exception as e:
            print(f"Warning: {key} fetch failed: {e}")

    # mix in contribution stats if available
    contrib_path = ROOT / "data" / "contributions.json"
    if contrib_path.exists():
        try:
            c_data = json.loads(contrib_path.read_text())
            stats["total_contributions"] = c_data.get("stats", {}).get("total", 0)
            stats["longest_streak"] = c_data.get("stats", {}).get("longest_streak", 0)
        except Exception:
            pass

    OUTPUT.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(f"✓ Stats → {OUTPUT}")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
