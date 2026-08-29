#!/usr/bin/env python3
"""
make_discord_card.py — Discord Profile Popout Edition (full-width)
──────────────────────────────────────────────────────────────────
Generates an animated Discord-style profile card SVG, 860px wide to
match the chat + heatmap cards:
  • Animated blurple banner (shifting gradient + drifting orbs)
  • Real circular avatar (embedded photo) with pulsing online status
  • Two-column body: identity / About Me / roles on the left,
    "Playing" activity + server stats on the right
  • Dragon cursor simulation: a mouse pointer glides in, "hovers"
    the card, morphs into a 🐉 and prowls over it forever

Output: discord-card.svg
"""

import base64
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "discord-card.svg"
AVATAR_PATH = ROOT / "profile pic 4.jpg"
STATS_PATH = ROOT / "data" / "stats.json"

# ── Discord palette ─────────────────────────────────────────────────
BLURPLE      = "#5865F2"
BLURPLE_HI   = "#7983F5"
VIOLET       = "#8B5CF6"
CARD_BG      = "#232428"
PANEL_BG     = "#111214"
CHIP_BG      = "#2B2D31"
DIVIDER      = "#3F4147"
TEXT         = "#F2F3F5"
MUTED        = "#B5BAC1"
LINK         = "#00A8FC"
ONLINE       = "#23A55A"
GOLD         = "#F0B232"
FLAME        = "#F26522"

FONT  = "'gg sans', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
EMOJI = "'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif"

W = 860

ABOUT_LINES = [
    "AI Engineer — building an AI-powered CAD system @ Aagento AI",
    "LLMs · RAG · Agentic AI · Fine-tuning (QLoRA on A100s)",
    "Shipped: Kerala Ayurveda RAG · DPR Validator (Indian Railways)",
]
PORTFOLIO = "arnavsao-portfolio.vercel.app"

ROLES = [
    ("Python",     "#3776AB"),
    ("TypeScript", "#3178C6"),
    ("LangChain",  "#1C9C6B"),
    ("PyTorch",    "#EE4C2C"),
    ("Angular",    "#DD0031"),
    ("RAG Wizard", VIOLET),
    ("Dragon Tamer", FLAME),
    ("ChromaDB",   GOLD),
]


def load_stats() -> dict:
    try:
        return json.loads(STATS_PATH.read_text())
    except Exception:
        return {}


def role_pills(x0: float, y0: float, max_w: float) -> tuple[list[str], float]:
    """Lay out role pills with wrap; returns (svg parts, y after last row)."""
    parts, x, y = [], x0, y0
    h, gap, pad = 26, 8, 10
    for i, (name, color) in enumerate(ROLES):
        w = pad * 2 + 14 + len(name) * 7.3
        if x + w > x0 + max_w:
            x = x0
            y += h + gap
        parts.append(f'  <g class="pill pill-{i}">')
        parts.append(f'    <rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h}" rx="13" '
                     f'fill="{CHIP_BG}" stroke="{DIVIDER}" stroke-width="1" />')
        parts.append(f'    <circle cx="{x + pad + 5:.0f}" cy="{y + h / 2:.0f}" r="5" fill="{color}" />')
        parts.append(f'    <text x="{x + pad + 15:.0f}" y="{y + h / 2 + 4.5:.0f}" fill="{TEXT}" '
                     f'font-family="{FONT}" font-size="12.5">{html.escape(name)}</text>')
        parts.append("  </g>")
        x += w + gap
    return parts, y + h


def main() -> None:
    avatar = base64.b64encode(AVATAR_PATH.read_bytes()).decode("ascii")
    stats = load_stats()
    contribs = stats.get("total_contributions", 0)
    streak = stats.get("longest_streak", 0)

    banner_h = 140
    panel_x, panel_w = 16, W - 32
    panel_y = 204
    tx = 40                       # left column text edge
    col_split = 496               # vertical divider x
    left_w = col_split - tx - 24  # left column usable width
    rx0 = col_split + 24          # right column text edge
    right_w = panel_x + panel_w - 24 - rx0

    body: list[str] = []

    # ── left column ─────────────────────────────────────────────────
    ly = panel_y + 38
    body.append(f'  <text class="fade f0" x="{tx}" y="{ly}" fill="{TEXT}" font-family="{FONT}" '
                f'font-size="23" font-weight="800">Arnav Sao</text>')
    ly += 22
    body.append(f'  <text class="fade f1" x="{tx}" y="{ly}" fill="{MUTED}" font-family="{FONT}" '
                f'font-size="13.5">arnavsao · he/him</text>')
    ly += 26
    body.append(f'  <text class="fade f2" x="{tx}" y="{ly}" font-family="{FONT}" font-size="13.5">'
                f'<tspan font-family="{EMOJI}">🐉</tspan>'
                f'<tspan fill="{MUTED}" dx="6">taming dragons · fine-tuning LLMs</tspan></text>')
    ly += 18
    body.append(f'  <line class="fade f2" x1="{tx}" y1="{ly}" x2="{tx + left_w}" y2="{ly}" '
                f'stroke="{DIVIDER}" stroke-width="1" />')
    ly += 27
    body.append(f'  <text class="fade f3" x="{tx}" y="{ly}" fill="{MUTED}" font-family="{FONT}" '
                f'font-size="11" font-weight="700" letter-spacing="1">ABOUT ME</text>')
    for i, line in enumerate(ABOUT_LINES):
        ly += 21
        body.append(f'  <text class="fade f{4 + i}" x="{tx}" y="{ly}" fill="{TEXT}" '
                    f'font-family="{FONT}" font-size="12.5">{html.escape(line)}</text>')
    ly += 21
    body.append(f'  <text class="fade f7" x="{tx}" y="{ly}" fill="{LINK}" font-family="{FONT}" '
                f'font-size="12.5" text-decoration="underline">{PORTFOLIO}</text>')
    ly += 18
    body.append(f'  <line class="fade f7" x1="{tx}" y1="{ly}" x2="{tx + left_w}" y2="{ly}" '
                f'stroke="{DIVIDER}" stroke-width="1" />')
    ly += 27
    body.append(f'  <text class="fade f8" x="{tx}" y="{ly}" fill="{MUTED}" font-family="{FONT}" '
                f'font-size="11" font-weight="700" letter-spacing="1">ROLES</text>')
    ly += 12
    pills, ly = role_pills(tx, ly, left_w)
    body.extend(pills)

    # ── right column ────────────────────────────────────────────────
    ry = panel_y + 34
    body.append(f'  <text class="fade f2" x="{rx0}" y="{ry}" fill="{MUTED}" font-family="{FONT}" '
                f'font-size="11" font-weight="700" letter-spacing="1">PLAYING A GAME</text>')
    ry += 14
    body.append(f'  <g class="fade f3">')
    body.append(f'    <rect x="{rx0}" y="{ry}" width="46" height="46" rx="10" fill="url(#iconGrad)" />')
    body.append(f'    <text x="{rx0 + 23}" y="{ry + 31}" text-anchor="middle" font-size="22" '
                f'font-family="{EMOJI}" class="brain">🧠</text>')
    body.append(f'    <text x="{rx0 + 60}" y="{ry + 15}" fill="{TEXT}" font-family="{FONT}" '
                f'font-size="13.5" font-weight="700">Neural Network Training</text>')
    body.append(f'    <text x="{rx0 + 60}" y="{ry + 32}" fill="{MUTED}" font-family="{FONT}" '
                f'font-size="12">epoch 42/&#8734; · loss 0.0042 &#8595;</text>')
    body.append(f'    <text x="{rx0 + 60}" y="{ry + 48}" fill="{ONLINE}" font-family="{FONT}" '
                f'font-size="12">{contribs:,} XP earned this year</text>')
    body.append("  </g>")
    ry += 62
    bar_w = right_w
    body.append(f'  <g class="fade f4">')
    body.append(f'    <rect x="{rx0}" y="{ry}" width="{bar_w}" height="6" rx="3" fill="{CHIP_BG}" />')
    body.append(f'    <rect class="loss-bar" x="{rx0}" y="{ry}" width="{bar_w}" height="6" rx="3" fill="url(#barGrad)" />')
    body.append(f'    <rect class="shimmer" x="{rx0}" y="{ry}" width="60" height="6" rx="3" fill="#ffffff" opacity="0.25" />')
    body.append("  </g>")
    ry += 24
    body.append(f'  <line class="fade f5" x1="{rx0}" y1="{ry}" x2="{rx0 + right_w}" y2="{ry}" '
                f'stroke="{DIVIDER}" stroke-width="1" />')
    ry += 27
    body.append(f'  <text class="fade f6" x="{rx0}" y="{ry}" fill="{MUTED}" font-family="{FONT}" '
                f'font-size="11" font-weight="700" letter-spacing="1">SERVER STATS</text>')
    stat_rows = [
        ("⚡", f"{contribs:,} contributions this year"),
        ("🔥", f"{streak}-day longest streak"),
        ("📍", "Bengaluru, India"),
        ("🐉", "1 dragon on cursor duty"),
    ]
    for i, (e, t) in enumerate(stat_rows):
        ry += 23
        body.append(f'  <text class="fade f{7 + i}" x="{rx0}" y="{ry}" font-family="{FONT}" font-size="12.5">'
                    f'<tspan font-family="{EMOJI}">{e}</tspan>'
                    f'<tspan fill="{TEXT}" dx="8">{html.escape(t)}</tspan></text>')

    # ── typing indicator across the bottom ──────────────────────────
    by = max(ly, ry) + 32
    for i in range(3):
        body.append(f'  <circle class="tdot tdot-{i}" cx="{tx + 6 + i * 13}" cy="{by}" r="3.5" fill="{MUTED}" />')
    body.append(f'  <text x="{tx + 46}" y="{by + 4}" fill="{MUTED}" font-family="{FONT}" font-size="12" '
                f'font-style="italic">the dragon is watching your cursor&#8230;</text>')
    by += 22

    panel_h = by - panel_y
    H = panel_y + panel_h + 16

    # column divider
    body.append(f'  <line class="fade f4" x1="{col_split}" y1="{panel_y + 22}" x2="{col_split}" '
                f'y2="{panel_y + panel_h - 22}" stroke="{DIVIDER}" stroke-width="1" />')

    # ── document ────────────────────────────────────────────────────
    p: list[str] = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">')

    p.append("  <defs>")
    p.append(f'    <clipPath id="cardClip"><rect width="{W}" height="{H}" rx="14" /></clipPath>')
    p.append('    <clipPath id="avClip"><circle cx="84" cy="140" r="44" /></clipPath>')
    p.append(f'    <linearGradient id="bannerGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
    p.append(f'      <stop offset="0%" stop-color="{BLURPLE}">')
    p.append(f'        <animate attributeName="stop-color" values="{BLURPLE};{VIOLET};#3B4BE0;{BLURPLE}" dur="9s" repeatCount="indefinite" />')
    p.append("      </stop>")
    p.append(f'      <stop offset="100%" stop-color="{VIOLET}">')
    p.append(f'        <animate attributeName="stop-color" values="{VIOLET};#3B4BE0;{BLURPLE};{VIOLET}" dur="9s" repeatCount="indefinite" />')
    p.append("      </stop>")
    p.append("    </linearGradient>")
    p.append(f'    <linearGradient id="iconGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
    p.append(f'      <stop offset="0%" stop-color="{BLURPLE}" /><stop offset="100%" stop-color="{VIOLET}" />')
    p.append("    </linearGradient>")
    p.append(f'    <linearGradient id="barGrad" x1="0%" y1="0%" x2="100%" y2="0%">')
    p.append(f'      <stop offset="0%" stop-color="{BLURPLE}" /><stop offset="100%" stop-color="{BLURPLE_HI}" />')
    p.append("    </linearGradient>")
    p.append("  </defs>")

    # ── styles ──────────────────────────────────────────────────────
    p.append("  <style>")
    p.append("    @keyframes fadeUp { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }")
    for i in range(11):
        p.append(f"    .f{i} {{ opacity:0; animation: fadeUp .5s ease-out {0.15 + i * 0.12:.2f}s forwards; }}")
    p.append("    @keyframes popIn { 0% { opacity:0; transform:scale(.6); } 70% { opacity:1; transform:scale(1.08); } 100% { opacity:1; transform:scale(1); } }")
    for i in range(len(ROLES)):
        p.append(f"    .pill-{i} {{ opacity:0; transform-origin:center; transform-box:fill-box; "
                 f"animation: popIn .4s ease-out {1.5 + i * 0.1:.2f}s forwards; }}")
    p.append("    @keyframes pulse { 0%,100% { transform:scale(1); opacity:.7; } 50% { transform:scale(1.7); opacity:0; } }")
    p.append("    .status-pulse { transform-origin:center; transform-box:fill-box; animation: pulse 2s ease-out infinite; }")
    p.append("    @keyframes drift { 0% { transform:translateY(0); } 50% { transform:translateY(-14px); } 100% { transform:translateY(0); } }")
    p.append("    .orb { animation: drift 6s ease-in-out infinite; }")
    p.append("    .orb2 { animation: drift 8s ease-in-out -3s infinite; }")
    p.append("    @keyframes twinkle { 0%,100% { opacity:.15; } 50% { opacity:.7; } }")
    p.append("    .star { animation: twinkle 3s ease-in-out infinite; }")
    p.append(f"    @keyframes grow {{ 0% {{ width:0; }} 100% {{ width:{bar_w}px; }} }}")
    p.append(f"    .loss-bar {{ width:0; animation: grow 3.5s ease-out 2.2s forwards; }}")
    p.append(f"    @keyframes slide {{ 0% {{ transform:translateX(0); opacity:0; }} 15% {{ opacity:.35; }} "
             f"85% {{ opacity:.35; }} 100% {{ transform:translateX({bar_w - 60}px); opacity:0; }} }}")
    p.append("    .shimmer { animation: slide 2.4s ease-in-out 2.4s infinite; }")
    p.append("    @keyframes bounce { 0%,60%,100% { transform:translateY(0); } 30% { transform:translateY(-6px); } }")
    for i in range(3):
        p.append(f"    .tdot-{i} {{ animation: bounce 1.2s ease-in-out {i * 0.18:.2f}s infinite; }}")
    p.append("    @keyframes wob { 0%,100% { transform:rotate(-6deg); } 50% { transform:rotate(6deg); } }")
    p.append("    .badge-e { transform-origin:center; transform-box:fill-box; animation: wob 3s ease-in-out infinite; }")
    p.append("    .brain { transform-origin:center; transform-box:fill-box; animation: wob 2.2s ease-in-out infinite; }")
    p.append("    @keyframes cursorIn { 0% { opacity:1; } 78% { opacity:1; } 92% { opacity:0; } 100% { opacity:0; } }")
    p.append("    .ptr { animation: cursorIn 3.2s ease-out forwards; }")
    p.append("    @keyframes dragonIn { 0%,82% { opacity:0; } 100% { opacity:1; } }")
    p.append("    .drg { opacity:0; animation: dragonIn 3.4s ease-out forwards; }")
    p.append("    @keyframes flap { 0%,100% { transform:scale(1) rotate(-4deg); } 50% { transform:scale(1.12) rotate(5deg); } }")
    p.append("    .drg-body { transform-origin:center; transform-box:fill-box; animation: flap 1s ease-in-out infinite; }")
    p.append("    @keyframes ripple { 0% { r:4; opacity:.8; } 100% { r:26; opacity:0; } }")
    p.append("    .ripple { animation: ripple 1.6s ease-out 3s infinite; }")
    p.append("  </style>")

    # ── card chrome ─────────────────────────────────────────────────
    p.append(f'  <g clip-path="url(#cardClip)">')
    p.append(f'    <rect width="{W}" height="{H}" fill="{CARD_BG}" />')
    p.append(f'    <rect width="{W}" height="{banner_h}" fill="url(#bannerGrad)" />')
    p.append(f'    <circle class="orb"  cx="640" cy="45" r="34" fill="#ffffff" opacity="0.08" />')
    p.append(f'    <circle class="orb2" cx="760" cy="95" r="20" fill="#ffffff" opacity="0.10" />')
    p.append(f'    <circle class="orb2" cx="440" cy="30" r="12" fill="#ffffff" opacity="0.10" />')
    for sx, sy, d in [(220, 40, 0), (330, 90, 1), (520, 105, 2), (700, 25, 1), (820, 60, 0), (170, 100, 2), (390, 60, 1)]:
        p.append(f'    <circle class="star" cx="{sx}" cy="{sy}" r="1.6" fill="#ffffff" style="animation-delay:{d * .9}s" />')
    p.append("  </g>")
    p.append(f'  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="13.5" fill="none" stroke="{DIVIDER}" />')

    # ── avatar + status ─────────────────────────────────────────────
    p.append(f'  <circle cx="84" cy="140" r="52" fill="{CARD_BG}" />')
    p.append(f'  <image href="data:image/jpeg;base64,{avatar}" x="40" y="96" width="88" height="88" '
             f'clip-path="url(#avClip)" preserveAspectRatio="xMidYMid slice" />')
    p.append(f'  <circle class="status-pulse" cx="116" cy="172" r="10" fill="{ONLINE}" />')
    p.append(f'  <circle cx="116" cy="172" r="13" fill="{CARD_BG}" />')
    p.append(f'  <circle cx="116" cy="172" r="9" fill="{ONLINE}" />')

    # ── badge tray ──────────────────────────────────────────────────
    tray_w = 158
    p.append(f'  <g class="fade f0">')
    p.append(f'    <rect x="{W - tray_w - 20}" y="154" width="{tray_w}" height="38" rx="9" fill="{PANEL_BG}" '
             f'stroke="{DIVIDER}" stroke-width="1" />')
    for i, e in enumerate(["🐉", "⚡", "🤖", "🔮", "🏆"]):
        p.append(f'    <text class="badge-e" x="{W - tray_w - 20 + 17 + i * 27}" y="180" font-size="17" '
                 f'font-family="{EMOJI}" style="animation-delay:{i * .4}s">{e}</text>')
    p.append("  </g>")

    # ── body panel ──────────────────────────────────────────────────
    p.append(f'  <rect x="{panel_x}" y="{panel_y}" width="{panel_w}" height="{panel_h}" rx="10" fill="{PANEL_BG}" />')
    p.extend(body)

    # ── dragon cursor simulation ────────────────────────────────────
    path_d = (f"M {W - 60} -20 C {W - 180} 60, 260 80, 210 160 "
              f"C 160 240, {W - 200} 250, {W - 220} {H - 160} "
              f"C {W - 240} {H - 60}, 200 {H - 80}, 170 {H // 2} "
              f"C 150 200, {W - 140} 150, {W - 60} -20")
    # phase 1: plain white pointer flies in and fades
    p.append('  <g class="ptr">')
    p.append(f'    <g><path d="M0,0 L0,16 L4.5,12.5 L7.5,19 L10,18 L7,11.5 L12,11 Z" fill="#ffffff" '
             f'stroke="#000000" stroke-width="1.2" stroke-linejoin="round" />')
    p.append(f'      <animateMotion dur="3.2s" fill="freeze" path="{path_d}" /></g>')
    p.append("  </g>")
    # phase 2: dragon takes over the cursor and prowls forever
    p.append('  <g class="drg">')
    p.append('    <g>')
    p.append('      <circle class="ripple" cx="0" cy="0" r="4" fill="none" stroke="#ffffff" stroke-width="1.5" />')
    for delay, size, op in [(-0.25, 3.5, 0.5), (-0.5, 2.5, 0.35), (-0.75, 1.8, 0.2)]:
        p.append(f'      <g opacity="{op}"><circle cx="0" cy="0" r="{size}" fill="{FLAME}" />')
        p.append(f'        <animateMotion dur="14s" begin="{delay}s" repeatCount="indefinite" path="{path_d}" /></g>')
    p.append(f'      <g><text class="drg-body" x="-15" y="10" font-size="30" font-family="{EMOJI}">🐉</text>')
    p.append(f'        <animateMotion dur="14s" repeatCount="indefinite" path="{path_d}" /></g>')
    p.append("    </g>")
    p.append("  </g>")

    p.append("</svg>")

    svg = "\n".join(p)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"✓ Discord card SVG → {OUTPUT}  ({len(svg)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
