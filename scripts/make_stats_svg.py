#!/usr/bin/env python3
"""
make_stats_svg.py
─────────────────
Generate a HUD-style SVG stats card matching the green aesthetic.
Output: github-stats.svg
"""

import json
import pathlib
import html

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATS_PATH = ROOT / "data" / "stats.json"
OUTPUT = ROOT / "github-stats.svg"

# ── Sci-Fi Design ───────────────────────────────────────────────────
BG           = "#0d1117"
BORDER       = "#2ea043"
TITLE_COLOR  = "#39d353"
SEP_COLOR    = "#30363d"
KEY_COLOR    = "#c9d1d9"
VAL_COLOR    = "#39d353"

FONT_FAMILY  = "'SF Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace"
FONT_SIZE    = 13
LINE_HEIGHT  = 22
PAD_X        = 28
PAD_Y        = 28

STAGGER      = 0.14
SLIDE_DIST   = 15
FADE_DUR     = 0.45

def main() -> None:
    stats = {}
    if STATS_PATH.exists():
        with open(STATS_PATH, "r", encoding="utf-8") as f:
            stats = json.load(f)

    title = "github stats"
    
    info_lines = [
        ("Total Contributions", f"{stats.get('total_contributions', 0):,}"),
        ("Longest Streak", f"{stats.get('longest_streak', 0)} days"),
        ("Repositories", f"{stats.get('repositories', 0)}"),
        ("Followers", f"{stats.get('followers', 0):,}"),
    ]

    total_lines = 2 + len(info_lines)
    svg_w = 490
    svg_h = PAD_Y * 2 + total_lines * LINE_HEIGHT + 16

    parts: list[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}"')
    parts.append(f'     width="{svg_w}" height="{svg_h}">')
    parts.append("")

    # ── Defs ────────────────────────────────────────────────────────
    parts.append("  <defs>")
    # Border gradient
    parts.append(f'    <linearGradient id="border-g2" x1="0%" y1="0%" x2="100%" y2="100%">')
    parts.append(f'      <stop offset="0%" stop-color="{TITLE_COLOR}" stop-opacity="0.5" />')
    parts.append(f'      <stop offset="100%" stop-color="{BORDER}" stop-opacity="0.2" />')
    parts.append(f'    </linearGradient>')
    parts.append("  </defs>")
    parts.append("")

    # Background
    parts.append(f'  <rect width="{svg_w}" height="{svg_h}" fill="{BG}" rx="8" />')
    parts.append(f'  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" fill="none" stroke="url(#border-g2)" stroke-width="1" rx="7" />')
    parts.append("")

    # ── CSS animation ───────────────────────────────────────────────
    total_anim = STAGGER * total_lines + FADE_DUR
    parts.append("  <style>")
    parts.append("    @keyframes fadeSlideIn {")
    parts.append(f"      from {{ opacity: 0; transform: translateX({SLIDE_DIST}px); }}")
    parts.append(f"      to   {{ opacity: 1; transform: translateX(0); }}")
    parts.append("    }")
    for i in range(total_lines):
        delay = STAGGER * i + 0.5  # Add a little delay so it animates after the info card
        parts.append(f"    .sline-{i} {{ opacity: 0; animation: fadeSlideIn {FADE_DUR}s ease-out {delay:.2f}s forwards; }}")
    parts.append(f"    @keyframes scanline {{ 0% {{ transform: translateY(-{svg_h}px) }} 100% {{ transform: translateY({svg_h}px) }} }}")
    parts.append(f"    .scanline {{ animation: scanline 3s linear infinite; }}")
    parts.append("  </style>")
    parts.append("")

    line_idx = 0
    def next_y() -> float:
        nonlocal line_idx
        return PAD_Y + line_idx * LINE_HEIGHT + FONT_SIZE

    def cls() -> str:
        return f"sline-{line_idx}"

    # Title
    y = next_y()
    parts.append(f'  <text x="{PAD_X}" y="{y:.0f}" fill="{TITLE_COLOR}" '
                 f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}" font-weight="bold" class="{cls()}">'
                 f'./{html.escape(title)}</text>')
    line_idx += 1

    # Separator
    y = next_y()
    sep = "─" * (len(title) + 2)
    parts.append(f'  <text x="{PAD_X}" y="{y:.0f}" fill="{SEP_COLOR}" '
                 f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}" class="{cls()}">{sep}</text>')
    line_idx += 1

    # Info rows
    for key, val in info_lines:
        y = next_y()
        parts.append(
            f'  <text y="{y:.0f}" font-family="{FONT_FAMILY}" '
            f'font-size="{FONT_SIZE}" class="{cls()}">'
            f'<tspan x="{PAD_X}" fill="{KEY_COLOR}">{html.escape(key)}</tspan>'
            f'<tspan fill="{SEP_COLOR}"> </tspan>'
            f'<tspan fill="{VAL_COLOR}" font-weight="bold">{html.escape(val)}</tspan>'
            f'</text>'
        )
        line_idx += 1

    # ── CRT Scanline sweep ──────────────────────────────────────────
    parts.append(f'  <rect class="scanline" x="0" y="0" width="{svg_w}" height="2" fill="{TITLE_COLOR}" opacity="0.05" />')

    parts.append("</svg>")

    svg = "\n".join(parts)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"✓ Stats SVG → {OUTPUT}  ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
