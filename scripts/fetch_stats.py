#!/usr/bin/env python3
"""
fetch_stats.py
──────────────
Scrapes basic GitHub stats from the public profile page to avoid
third-party API rate limits and external service dependencies.

Output: data/stats.json
"""

import requests
from bs4 import BeautifulSoup
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "stats.json"
USERNAME = "arnavsao"

def scrape_stats() -> dict:
    url = f"https://github.com/{USERNAME}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Warning: Failed to fetch profile (Status {resp.status_code})")
        return {}

    soup = BeautifulSoup(resp.text, 'html.parser')

    stats = {
        "repositories": 0,
        "followers": 0,
        "following": 0,
        "stars": 0
    }

    # Extract Followers
    followers_a = soup.find('a', href=re.compile(rf'/{USERNAME}\?tab=followers'))
    if followers_a:
        span = followers_a.find('span', class_='text-bold')
        if span:
            stats["followers"] = int(span.text.strip().replace(',', ''))

    # Extract Following
    following_a = soup.find('a', href=re.compile(rf'/{USERNAME}\?tab=following'))
    if following_a:
        span = following_a.find('span', class_='text-bold')
        if span:
            stats["following"] = int(span.text.strip().replace(',', ''))

    # Extract Repositories
    repos_a = soup.find('a', href=re.compile(rf'/{USERNAME}\?tab=repositories'))
    if repos_a:
        span = repos_a.find('span', class_='Counter')
        if span:
            try:
                stats["repositories"] = int(span.text.strip().replace(',', ''))
            except ValueError:
                pass

    # Extract Stars (starred repos by the user, not stars received. But it's a proxy for activity if we can't get received stars without API)
    stars_a = soup.find('a', href=re.compile(rf'/{USERNAME}\?tab=stars'))
    if stars_a:
        span = stars_a.find('span', class_='Counter')
        if span:
            try:
                stats["stars"] = int(span.text.strip().replace(',', ''))
            except ValueError:
                pass

    return stats


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    stats = scrape_stats()
    
    # Check if contributions.json exists to mix in total contributions
    contrib_path = ROOT / "data" / "contributions.json"
    if contrib_path.exists():
        try:
            with open(contrib_path, "r", encoding="utf-8") as f:
                c_data = json.load(f)
                stats["total_contributions"] = c_data.get("stats", {}).get("total", 0)
                stats["longest_streak"] = c_data.get("stats", {}).get("longest_streak", 0)
        except Exception:
            pass

    OUTPUT.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(f"✓ Stats → {OUTPUT}")
    for k, v in stats.items():
        print(f"  {k.title()}: {v}")


if __name__ == "__main__":
    main()
