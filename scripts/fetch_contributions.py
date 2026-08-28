#!/usr/bin/env python3
"""
fetch_contributions.py
──────────────────────
Scrape the public GitHub contribution calendar for a user.
No token required — uses the public HTML fragment at:
    https://github.com/users/<username>/contributions

Output:
    data/contributions.json
"""

import json
import pathlib
from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "contributions.json"
USERNAME = "arnavsao"
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_and_parse() -> dict:
    """Fetch contribution calendar HTML and extract day cells."""
    resp = requests.get(URL, headers={"Accept": "text/html"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Build a lookup: td-id → tooltip text
    # GitHub puts <tool-tip for="<td-id>"> as siblings, not children.
    tip_map: dict[str, str] = {}
    for tip in soup.find_all("tool-tip"):
        target_id = tip.get("for", "")
        if target_id:
            tip_map[target_id] = tip.get_text(strip=True)

    days: list[dict] = []

    # GitHub renders contribution cells as <td> with data-date and data-level
    for td in soup.select("td.ContributionCalendar-day"):
        date_str = td.get("data-date", "")
        level = int(td.get("data-level", "0"))

        # Match the tooltip via the td's id
        count = 0
        td_id = td.get("id", "")
        tip_text = tip_map.get(td_id, "")

        if not tip_text:
            # Fallback: try nested <span class="sr-only">
            span = td.find("span", class_="sr-only")
            if span:
                tip_text = span.get_text(strip=True)

        if tip_text:
            # Format: "X contributions on ..." or "No contributions on ..."
            if tip_text.startswith("No"):
                count = 0
            else:
                try:
                    count = int(tip_text.split()[0].replace(",", ""))
                except (ValueError, IndexError):
                    count = 0

        if date_str:
            days.append({
                "date": date_str,
                "count": count,
                "level": level,
            })

    # Sort by date
    days.sort(key=lambda d: d["date"])

    # ── Derived stats ───────────────────────────────────────────────
    total = sum(d["count"] for d in days)

    # Current streak
    now_utc = datetime.now(timezone.utc)
    today = now_utc.strftime("%Y-%m-%d")
    streak = 0
    date_set = {d["date"]: d["count"] for d in days}
    check = now_utc - timedelta(days=1)
    # Allow today to have 0 (day not over yet) — start from yesterday
    while True:
        ds = check.strftime("%Y-%m-%d")
        if date_set.get(ds, 0) > 0:
            streak += 1
            check -= timedelta(days=1)
        else:
            break
    # If today also has contributions, add it
    if date_set.get(today, 0) > 0:
        streak += 1

    # Longest streak
    longest = 0
    current = 0
    for d in days:
        if d["count"] > 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    # Best day
    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}

    stats = {
        "username": USERNAME,
        "total": total,
        "current_streak": streak,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "num_days": len(days),
    }

    return {"days": days, "stats": stats}


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data = fetch_and_parse()
    OUTPUT.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"✓ Contributions → {OUTPUT}")
    s = data["stats"]
    print(f"  {s['total']:,} contributions over {s['num_days']} days")
    print(f"  Current streak: {s['current_streak']} days")
    print(f"  Longest streak: {s['longest_streak']} days")
    print(f"  Best day: {s['best_day']['date']} ({s['best_day']['count']})")


if __name__ == "__main__":
    main()
