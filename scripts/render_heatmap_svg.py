#!/usr/bin/env python3
"""
render_heatmap_svg.py — Sci-Fi Edition
──────────────────────────────────────
Generate a GitHub contribution heatmap SVG from JSON data.
Features:
  • Sci-Fi cyan color ramp
  • Neon glow on high-activity cells
  • Diagonal reveal animation (CSS keyframes)
  • Stats footer with cyan text

Output: contrib-heatmap.svg
"""

import json
import pathlib
import datetime
import html

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"

# ── Sci-Fi Design ───────────────────────────────────────────────────
BG_COLOR    = "#0d1117"
TEXT_COLOR  = "#39d353"
DIM_TEXT    = "#8b949e"
CELL_SIZE   = 12
CELL_GAP    = 3
CELL_RX     = 2  # slightly sharper corners

# Colors for contribution levels (0 to 4+)
LEVEL_COLORS = [
    "#161b22",  # 0
    "#0e4429",  # 1
    "#006d32",  # 2
    "#2ea043",  # 3
    "#39d353",  # 4+
]
GLOW_LEVEL = 4  # Apply SVG glow filter to cells at this level or higher

FONT_FAMILY = "'SF Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace"
FONT_SIZE = 11
STATS_FONT_SIZE = 12

# ── Animation ───────────────────────────────────────────────────────
# We animate opacity from 0 -> 1 in a diagonal wave from top-left to bottom-right
ANIM_DUR = 1.2
WAVE_SPEED = 0.03


def get_level(count: int) -> int:
    if count == 0: return 0
    if count <= 2: return 1
    if count <= 5: return 2
    if count <= 9: return 3
    return 4


def main() -> None:
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found. Run fetch_contributions.py first.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    days_list = data.get("days", [])
    stats = data.get("stats", {})
    total_contribs = stats.get("total", 0)
    longest_streak = stats.get("longest_streak", 0)
    best_day_count = stats.get("best_day", {}).get("count", 0)
    best_day_date = stats.get("best_day", {}).get("date", "")

    if not days_list:
        print("No contribution data found.")
        return

    # Group flat days into weeks (columns). Assuming days are contiguous and ordered.
    # We chunk them into columns of up to 7 days, aligning based on weekday.
    weeks = []
    current_week = []
    
    for day in days_list:
        try:
            dt = datetime.datetime.strptime(day["date"], "%Y-%m-%d")
            # For GitHub, 0=Sunday, 6=Saturday in our grid, but Python weekday is 0=Mon, 6=Sun.
            # We will just map it dynamically or just pack 7 days per column sequentially.
            # Since the data is scraped from GitHub, it's already in order. Let's just group by 7.
            # Wait, the first week might not be a full 7 days.
            # Let's use the Python weekday to place them correctly.
            # isoweekday: Mon=1, Sun=7. For Github: Sun=0, Mon=1...Sat=6.
            gh_weekday = dt.isoweekday() % 7
            day["weekday"] = gh_weekday
            
            if not current_week:
                current_week.append(day)
            else:
                if gh_weekday == 0: # Sunday starts a new week column
                    weeks.append({"days": current_week})
                    current_week = [day]
                else:
                    current_week.append(day)
        except ValueError:
            pass
            
    if current_week:
        weeks.append({"days": current_week})

    num_cols = len(weeks)
    num_rows = 7

    # ── SVG Dimensions ──────────────────────────────────────────────
    margin_top = 30
    margin_left = 35
    margin_right = 20
    margin_bottom = 50

    grid_w = num_cols * (CELL_SIZE + CELL_GAP) - CELL_GAP
    grid_h = num_rows * (CELL_SIZE + CELL_GAP) - CELL_GAP

    svg_w = margin_left + grid_w + margin_right
    svg_h = margin_top + grid_h + margin_bottom

    parts: list[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}"')
    parts.append(f'     width="{svg_w}" height="{svg_h}">')
    parts.append("")

    # ── Defs (Glow Filter) ──────────────────────────────────────────
    parts.append("  <defs>")
    parts.append('    <filter id="cell-glow" x="-20%" y="-20%" width="140%" height="140%">')
    parts.append(f'      <feGaussianBlur in="SourceGraphic" stdDeviation="1.5" result="blur" />')
    parts.append(f'      <feFlood flood-color="{LEVEL_COLORS[4]}" flood-opacity="0.6" result="color" />')
    parts.append('      <feComposite in="color" in2="blur" operator="in" result="glow" />')
    parts.append('      <feMerge>')
    parts.append('        <feMergeNode in="glow" />')
    parts.append('        <feMergeNode in="SourceGraphic" />')
    parts.append('      </feMerge>')
    parts.append('    </filter>')
    parts.append("  </defs>")
    parts.append("")

    # ── Background ──────────────────────────────────────────────────
    parts.append(f'  <rect width="{svg_w}" height="{svg_h}" fill="{BG_COLOR}" rx="8" />')
    parts.append("")

    # ── CSS Animation ───────────────────────────────────────────────
    parts.append("  <style>")
    parts.append("    @keyframes popIn {")
    parts.append("      0% { opacity: 0; transform: scale(0.8); }")
    parts.append("      70% { opacity: 1; transform: scale(1.1); }")
    parts.append("      100% { opacity: 1; transform: scale(1); }")
    parts.append("    }")
    parts.append("    .cell { opacity: 0; transform-origin: center; }")
    parts.append("  </style>")
    parts.append("")

    # ── Grid Render ─────────────────────────────────────────────────
    parts.append(f'  <g transform="translate({margin_left}, {margin_top})">')

    # Month Labels
    month_labels = []
    prev_month = None
    for c, week in enumerate(weeks):
        if not week["days"]: continue
        first_day = week["days"][0]["date"]
        try:
            dt = datetime.datetime.strptime(first_day, "%Y-%m-%d")
            month = dt.strftime("%b")
            if month != prev_month:
                month_labels.append((c, month))
                prev_month = month
        except ValueError:
            pass

    for c, month in month_labels:
        x = c * (CELL_SIZE + CELL_GAP)
        parts.append(f'    <text x="{x}" y="-8" fill="{DIM_TEXT}" '
                     f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}">{html.escape(month)}</text>')

    # Day Labels (Mon, Wed, Fri)
    day_names = ["", "Mon", "", "Wed", "", "Fri", ""]
    for r, day in enumerate(day_names):
        if day:
            y = r * (CELL_SIZE + CELL_GAP) + 10
            parts.append(f'    <text x="-25" y="{y}" fill="{DIM_TEXT}" '
                         f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}">{day}</text>')

    # Cells
    cell_count = 0
    for c, week in enumerate(weeks):
        for day in week["days"]:
            r = day.get("weekday", 0)  # 0=Sun, 6=Sat
            count = day.get("count", 0)
            level = get_level(count)
            color = LEVEL_COLORS[level]
            
            x = c * (CELL_SIZE + CELL_GAP)
            y = r * (CELL_SIZE + CELL_GAP)

            # Diagonal delay: top-left to bottom-right
            delay = (c + r) * WAVE_SPEED
            
            # Apply glow to high activity cells
            filter_attr = ' filter="url(#cell-glow)"' if level >= GLOW_LEVEL else ''

            # Transform origin for scaling from center of cell
            cx = x + CELL_SIZE/2
            cy = y + CELL_SIZE/2
            
            parts.append(f'    <rect class="cell" x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                         f'rx="{CELL_RX}" fill="{color}"{filter_attr} '
                         f'style="animation: popIn {ANIM_DUR}s ease-out {delay:.2f}s forwards; transform-origin: {cx}px {cy}px;" />')
            
            # Optional: Tooltip title (standard SVG title element)
            # parts.append(f'      <title>{count} contributions on {day["date"]}</title>')
            # parts.append(f'    </rect>')
            
            cell_count += 1

    parts.append('  </g>')
    parts.append("")

    # ── Legend ──────────────────────────────────────────────────────
    legend_y = svg_h - 25
    legend_x = svg_w - margin_right - (5 * (CELL_SIZE + CELL_GAP)) - 35
    
    parts.append(f'  <text x="{legend_x - 30}" y="{legend_y + 10}" fill="{DIM_TEXT}" '
                 f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}">Less</text>')
    
    for i, color in enumerate(LEVEL_COLORS):
        x = legend_x + i * (CELL_SIZE + CELL_GAP)
        filter_attr = ' filter="url(#cell-glow)"' if i >= GLOW_LEVEL else ''
        parts.append(f'  <rect x="{x}" y="{legend_y}" width="{CELL_SIZE}" height="{CELL_SIZE}" '
                     f'rx="{CELL_RX}" fill="{color}"{filter_attr} />')

    parts.append(f'  <text x="{legend_x + 5 * (CELL_SIZE + CELL_GAP) + 5}" y="{legend_y + 10}" fill="{DIM_TEXT}" '
                 f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}">More</text>')

    # ── Stats Footer ────────────────────────────────────────────────
    stats_y = legend_y + 10
    stats_text = (f"{total_contribs:,} Contribs in last year  ·  "
                  f"Longest Streak: {longest_streak} days  ·  "
                  f"Best Day: {best_day_count} ({best_day_date})")
    
    parts.append(f'  <text x="{margin_left}" y="{stats_y}" fill="{TEXT_COLOR}" '
                 f'font-family="{FONT_FAMILY}" font-size="{STATS_FONT_SIZE}" '
                 f'font-weight="bold">{html.escape(stats_text)}</text>')

    parts.append("</svg>")

    svg_content = "\n".join(parts)
    OUTPUT.write_text(svg_content, encoding="utf-8")
    print(f"✓ Heatmap SVG → {OUTPUT}  ({len(weeks)} weeks, {cell_count} cells)")

if __name__ == "__main__":
    main()
