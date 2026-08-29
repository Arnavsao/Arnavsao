#!/usr/bin/env python3
"""
make_discord_stats.py — Discord Server-Stats Edition
────────────────────────────────────────────────────
Generates an animated Discord-style GitHub stats card SVG:
  • "# server-stats" channel header
  • 3×2 grid of stat tiles (commits, PRs, issues, repos, stars,
    followers) with pop-in numbers and growing accent bars
  • Nitro-style "server boost" gradient bar fed by contributions

Reads data/stats.json (produced by fetch_stats.py).
Output: discord-stats.svg
"""

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "discord-stats.svg"
STATS_PATH = ROOT / "data" / "stats.json"

BLURPLE   = "#5865F2"
VIOLET    = "#8B5CF6"
PINK      = "#FF73FA"
BG        = "#313338"
HEADER_BG = "#2B2D31"
TILE_BG   = "#2B2D31"
INNER_BG  = "#232428"
DIVIDER   = "#3F4147"
TEXT      = "#F2F3F5"
MUTED     = "#949BA4"
ONLINE    = "#23A55A"
GOLD      = "#F0B232"
RED       = "#F23F43"
CYAN      = "#00A8FC"

FONT  = "'gg sans', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
EMOJI = "'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif"

W = 860


def main() -> None:
    try:
        s = json.loads(STATS_PATH.read_text())
    except Exception:
        s = {}

    commits = s.get("commits", 0)
    prs = s.get("prs", 0)
    prs_merged = s.get("prs_merged", 0)
    issues = s.get("issues", 0)
    repos = s.get("repositories", 0)
    stars = s.get("stars", 0)
    followers = s.get("followers", 0)
    contribs = s.get("total_contributions", 0)
    streak = s.get("longest_streak", 0)

    merged_pct = round(prs_merged / prs * 100) if prs else 0
    tiles = [
        ("⚡", "COMMITS",       f"{commits:,}",   "authored across all repos",      BLURPLE),
        ("🔀", "PULL REQUESTS", f"{prs:,}",       f"{prs_merged} merged · {merged_pct}%", ONLINE),
        ("🐛", "ISSUES",        f"{issues:,}",    "opened & hunted down",           RED),
        ("📦", "REPOSITORIES",  f"{repos:,}",     "public projects",                GOLD),
        ("⭐", "STARS",         f"{stars:,}",     "collected on repos",             PINK),
        ("👥", "FOLLOWERS",     f"{followers:,}", "watching the journey",           CYAN),
    ]

    header_h = 42
    pad = 20
    gap = 12
    cols = 3
    tile_w = (W - pad * 2 - gap * (cols - 1)) / cols
    tile_h = 84
    grid_y = header_h + 16

    p: list[str] = []
    rows = (len(tiles) + cols - 1) // cols
    boost_y = grid_y + rows * tile_h + (rows - 1) * gap + 16
    H = boost_y + 58 + 16

    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    p.append("  <defs>")
    p.append(f'    <linearGradient id="boostGrad" x1="0%" y1="0%" x2="100%" y2="0%">')
    p.append(f'      <stop offset="0%" stop-color="{PINK}">')
    p.append(f'        <animate attributeName="stop-color" values="{PINK};{VIOLET};{BLURPLE};{PINK}" dur="6s" repeatCount="indefinite" />')
    p.append("      </stop>")
    p.append(f'      <stop offset="100%" stop-color="{BLURPLE}">')
    p.append(f'        <animate attributeName="stop-color" values="{BLURPLE};{PINK};{VIOLET};{BLURPLE}" dur="6s" repeatCount="indefinite" />')
    p.append("      </stop>")
    p.append("    </linearGradient>")
    p.append("  </defs>")

    p.append("  <style>")
    p.append("    @keyframes popIn { 0% { opacity:0; transform:scale(.7); } 70% { opacity:1; transform:scale(1.05); } 100% { opacity:1; transform:scale(1); } }")
    for i in range(len(tiles)):
        p.append(f"    .tile-{i} {{ opacity:0; transform-origin:center; transform-box:fill-box; "
                 f"animation: popIn .45s ease-out {0.2 + i * 0.13:.2f}s forwards; }}")
    p.append("    @keyframes growBar { from { transform:scaleX(0); } to { transform:scaleX(1); } }")
    for i in range(len(tiles)):
        p.append(f"    .bar-{i} {{ transform:scaleX(0); transform-origin:left center; transform-box:fill-box; "
                 f"animation: growBar 1s ease-out {0.5 + i * 0.13:.2f}s forwards; }}")
    p.append("    @keyframes wob { 0%,100% { transform:rotate(-6deg); } 50% { transform:rotate(6deg); } }")
    p.append("    .t-emoji { transform-origin:center; transform-box:fill-box; animation: wob 3s ease-in-out infinite; }")
    p.append("    @keyframes boostFill { from { transform:scaleX(0); } to { transform:scaleX(1); } }")
    p.append("    .boost-fill { transform:scaleX(0); transform-origin:left center; transform-box:fill-box; "
             "animation: boostFill 2.5s ease-out 1.2s forwards; }")
    p.append("    @keyframes rocket { 0%,100% { transform:translate(0,0) rotate(0deg); } 25% { transform:translate(1px,-2px) rotate(4deg); } "
             "75% { transform:translate(-1px,1px) rotate(-4deg); } }")
    p.append("    .rocket { animation: rocket 1.6s ease-in-out infinite; }")
    p.append("    @keyframes fadeIn { from { opacity:0; } to { opacity:1; } }")
    p.append("    .boost { opacity:0; animation: fadeIn .6s ease-out 1s forwards; }")
    p.append("    @keyframes hashSpin { 0%,90%,100% { transform:rotate(0deg); } 95% { transform:rotate(12deg); } }")
    p.append("    .hash { transform-origin:center; transform-box:fill-box; animation: hashSpin 5s ease-in-out infinite; }")
    p.append("  </style>")

    # background + channel header
    p.append(f'  <rect width="{W}" height="{H}" rx="12" fill="{BG}" />')
    p.append(f'  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="11.5" fill="none" stroke="{DIVIDER}" />')
    p.append(f'  <path d="M0,12 Q0,0 12,0 L{W - 12},0 Q{W},0 {W},12 L{W},{header_h} L0,{header_h} Z" fill="{HEADER_BG}" />')
    p.append(f'  <line x1="0" y1="{header_h}" x2="{W}" y2="{header_h}" stroke="{DIVIDER}" stroke-width="1" />')
    p.append(f'  <text class="hash" x="20" y="28" fill="{MUTED}" font-family="{FONT}" font-size="19" font-weight="700">#</text>')
    p.append(f'  <text x="38" y="27" fill="{TEXT}" font-family="{FONT}" font-size="15" font-weight="700">server-stats</text>')
    p.append(f'  <line x1="146" y1="12" x2="146" y2="30" stroke="{DIVIDER}" stroke-width="1" />')
    p.append(f'  <text x="158" y="27" fill="{MUTED}" font-family="{FONT}" font-size="12.5">live numbers from the GitHub API — refreshed daily</text>')
    p.append(f'  <circle cx="{W - 96}" cy="21" r="4" fill="{ONLINE}" />')
    p.append(f'  <text x="{W - 86}" y="25" fill="{MUTED}" font-family="{FONT}" font-size="12">1 online</text>')

    # stat tiles
    for i, (emoji, label, value, sub, color) in enumerate(tiles):
        r, c = divmod(i, cols)
        x = pad + c * (tile_w + gap)
        y = grid_y + r * (tile_h + gap)
        p.append(f'  <g class="tile-{i}">')
        p.append(f'    <rect x="{x:.0f}" y="{y}" width="{tile_w:.0f}" height="{tile_h}" rx="8" '
                 f'fill="{TILE_BG}" stroke="{DIVIDER}" stroke-width="1" />')
        p.append(f'    <rect x="{x + 14:.0f}" y="{y + 14}" width="40" height="40" rx="9" fill="{INNER_BG}" />')
        p.append(f'    <text class="t-emoji" x="{x + 34:.0f}" y="{y + 41}" text-anchor="middle" font-size="19" '
                 f'font-family="{EMOJI}" style="animation-delay:{i * .5}s">{emoji}</text>')
        p.append(f'    <text x="{x + 66:.0f}" y="{y + 26}" fill="{MUTED}" font-family="{FONT}" '
                 f'font-size="10.5" font-weight="700" letter-spacing="1">{html.escape(label)}</text>')
        p.append(f'    <text x="{x + 66:.0f}" y="{y + 50}" fill="{TEXT}" font-family="{FONT}" '
                 f'font-size="24" font-weight="800">{value}</text>')
        p.append(f'    <text x="{x + 66:.0f}" y="{y + 66}" fill="{MUTED}" font-family="{FONT}" '
                 f'font-size="11">{html.escape(sub)}</text>')
        p.append(f'    <rect class="bar-{i}" x="{x + 14:.0f}" y="{y + tile_h - 10}" width="{tile_w - 28:.0f}" '
                 f'height="3" rx="1.5" fill="{color}" />')
        p.append("  </g>")

    # nitro-style boost bar
    bx, bw = pad, W - pad * 2
    p.append(f'  <g class="boost">')
    p.append(f'    <rect x="{bx}" y="{boost_y}" width="{bw}" height="58" rx="8" fill="{TILE_BG}" '
             f'stroke="{DIVIDER}" stroke-width="1" />')
    p.append(f'    <text class="rocket" x="{bx + 16}" y="{boost_y + 36}" font-size="22" font-family="{EMOJI}">🚀</text>')
    p.append(f'    <text x="{bx + 52}" y="{boost_y + 24}" fill="{TEXT}" font-family="{FONT}" '
             f'font-size="13" font-weight="700">SERVER BOOST — Level &#8734;</text>')
    p.append(f'    <text x="{bx + bw - 16}" y="{boost_y + 24}" text-anchor="end" fill="{MUTED}" '
             f'font-family="{FONT}" font-size="12">{contribs:,} contributions · {streak}-day best streak</text>')
    p.append(f'    <rect x="{bx + 52}" y="{boost_y + 36}" width="{bw - 68}" height="8" rx="4" fill="{INNER_BG}" />')
    p.append(f'    <rect class="boost-fill" x="{bx + 52}" y="{boost_y + 36}" width="{bw - 68}" height="8" rx="4" '
             f'fill="url(#boostGrad)" />')
    p.append("  </g>")

    p.append("</svg>")

    svg = "\n".join(p)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"✓ Discord stats SVG → {OUTPUT}  ({len(svg)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
