#!/usr/bin/env python3
"""
make_discord_chat.py — Discord Channel View Edition
───────────────────────────────────────────────────
Generates an animated Discord-style #tech-stack channel SVG:
  • Channel header with topic
  • Messages that slide in (avatar, name tag, timestamps)
  • Tech-stack chips, a rich embed with animated blurple border
  • Reaction pills that pop in
  • Typing indicator at the bottom

Output: discord-chat.svg
"""

import base64
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "discord-chat.svg"
AVATAR_PATH = ROOT / "profile pic 4.jpg"
STATS_PATH = ROOT / "data" / "stats.json"

BLURPLE   = "#5865F2"
VIOLET    = "#8B5CF6"
BG        = "#313338"
HEADER_BG = "#2B2D31"
CHIP_BG   = "#232428"
EMBED_BG  = "#2B2D31"
DIVIDER   = "#3F4147"
TEXT      = "#DBDEE1"
HEADING   = "#F2F3F5"
MUTED     = "#949BA4"
LINK      = "#00A8FC"
ONLINE    = "#23A55A"

FONT  = "'gg sans', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
EMOJI = "'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif"

W = 860

STACK = [
    ("Python", "#3776AB"), ("TypeScript", "#3178C6"), ("Angular", "#DD0031"),
    ("LangChain", "#1C9C6B"), ("PyTorch", "#EE4C2C"), ("ChromaDB", "#F0B232"),
    ("Ollama", "#FFFFFF"), ("Gemini", "#4E8CF5"), ("Modal", "#7FEE64"),
    ("PEFT / LoRA", VIOLET), ("Canvas 2D", "#FF7A59"), ("DXF", "#9AA4B2"),
]

REACTIONS = [("🐉", "42"), ("🔥", "17"), ("🚀", "99+"), ("🧠", "8")]


def main() -> None:
    avatar = base64.b64encode(AVATAR_PATH.read_bytes()).decode("ascii")
    try:
        stats = json.loads(STATS_PATH.read_text())
        contribs = stats.get("total_contributions", 0)
        streak = stats.get("longest_streak", 0)
    except Exception:
        contribs, streak = 0, 0

    p: list[str] = []
    body: list[str] = []
    msg = 0  # message animation index
    av_centers: dict[int, float] = {}

    def group(cls: str) -> str:
        return f'  <g class="{cls}">'

    # ── header ──────────────────────────────────────────────────────
    y = 58

    # ── message 1: stack loadout ────────────────────────────────────
    def msg_header(y: float, idx: int) -> list[str]:
        av_centers[idx] = y + 20
        out = []
        out.append(f'    <circle cx="46" cy="{y + 20}" r="20" fill="{CHIP_BG}" />')
        out.append(f'    <image href="data:image/jpeg;base64,{avatar}" x="26" y="{y}" width="40" height="40" '
                   f'clip-path="url(#av{idx})" preserveAspectRatio="xMidYMid slice" />')
        out.append(f'    <text x="78" y="{y + 15}" fill="{HEADING}" font-family="{FONT}" '
                   f'font-size="15" font-weight="700">arnavsao</text>')
        tag_x = 78 + 76
        out.append(f'    <rect x="{tag_x}" y="{y + 2}" width="86" height="17" rx="4" fill="{BLURPLE}" />')
        out.append(f'    <text x="{tag_x + 43}" y="{y + 14.5}" text-anchor="middle" fill="#ffffff" '
                   f'font-family="{FONT}" font-size="10" font-weight="700">AI ENGINEER</text>')
        out.append(f'    <text x="{tag_x + 96}" y="{y + 15}" fill="{MUTED}" font-family="{FONT}" '
                   f'font-size="11.5">Today at 09:41</text>')
        return out

    body.append(group(f"msg m{msg}"))
    body.extend(msg_header(y, 1))
    body.append(f'    <text x="78" y="{y + 36}" font-family="{FONT}" font-size="14" fill="{TEXT}">'
                f'current loadout <tspan font-family="{EMOJI}">👇</tspan></text>')
    body.append("  </g>")
    msg += 1

    # stack chips (wrapped)
    y += 50
    x0, x, cy = 78, 78, y
    ch, gap, pad = 26, 8, 10
    for i, (name, color) in enumerate(STACK):
        cw = pad * 2 + 13 + len(name) * 7.2
        if x + cw > W - 30:
            x = x0
            cy += ch + gap
        body.append(f'  <g class="chip chip-{i}">')
        body.append(f'    <rect x="{x:.0f}" y="{cy}" width="{cw:.0f}" height="{ch}" rx="6" '
                    f'fill="{CHIP_BG}" stroke="{DIVIDER}" stroke-width="1" />')
        body.append(f'    <circle cx="{x + pad + 4:.0f}" cy="{cy + ch / 2}" r="4.5" fill="{color}" />')
        body.append(f'    <text x="{x + pad + 13:.0f}" y="{cy + ch / 2 + 4.5}" fill="{TEXT}" '
                    f'font-family="{FONT}" font-size="12.5">{html.escape(name)}</text>')
        body.append("  </g>")
        x += cw + gap
    y = cy + ch + 26

    # ── message 2: embed ────────────────────────────────────────────
    body.append(group(f"msg m{msg}"))
    body.extend(msg_header(y, 2))
    body.append(f'    <text x="78" y="{y + 36}" font-family="{FONT}" font-size="14" fill="{TEXT}">'
                f'what I&#8217;m building right now <tspan font-family="{EMOJI}">⚒️</tspan></text>')
    body.append("  </g>")
    msg += 1

    y += 50
    e_x, e_w, e_h = 78, 560, 148
    body.append(group(f"msg m{msg}"))
    body.append(f'    <rect x="{e_x}" y="{y}" width="{e_w}" height="{e_h}" rx="6" fill="{EMBED_BG}" />')
    body.append(f'    <rect class="embed-edge" x="{e_x}" y="{y}" width="4" height="{e_h}" rx="2" fill="{BLURPLE}" />')
    body.append(f'    <text x="{e_x + 20}" y="{y + 28}" fill="{HEADING}" font-family="{FONT}" '
                f'font-size="14.5" font-weight="700">'
                f'<tspan font-family="{EMOJI}">🚧</tspan><tspan dx="6">AI-powered CAD system — Aagento AI</tspan></text>')
    body.append(f'    <text x="{e_x + 20}" y="{y + 52}" fill="{TEXT}" font-family="{FONT}" font-size="12.5">'
                f'Natural-language commands &#8594; DXF parsing &#8594; Canvas 2D rendering</text>')
    body.append(f'    <text x="{e_x + 20}" y="{y + 78}" fill="{MUTED}" font-family="{FONT}" font-size="11" '
                f'font-weight="700" letter-spacing="0.5">PREVIOUSLY SHIPPED</text>')
    body.append(f'    <text x="{e_x + 20}" y="{y + 98}" fill="{TEXT}" font-family="{FONT}" font-size="12.5">'
                f'LLaMA-2 QLoRA fine-tune (Modal A100) · Kerala Ayurveda RAG (4 agents)</text>')
    body.append(f'    <text x="{e_x + 20}" y="{y + 116}" fill="{TEXT}" font-family="{FONT}" font-size="12.5">'
                f'DPR Validator — RAG + OCR for Indian Railways</text>')
    body.append(f'    <text x="{e_x + 20}" y="{y + 138}" fill="{MUTED}" font-family="{FONT}" font-size="11.5">'
                f'{contribs:,} contributions this year · {streak}-day longest streak · '
                f'<tspan fill="{LINK}">arnavsao-portfolio.vercel.app</tspan></text>')
    body.append("  </g>")
    msg += 1
    y += e_h + 14

    # reactions
    rx = 78
    for i, (emoji, count) in enumerate(REACTIONS):
        rw = 30 + len(count) * 7.5
        first = (i == 0)
        fill = "#3B405A" if first else CHIP_BG
        stroke = BLURPLE if first else DIVIDER
        body.append(f'  <g class="react react-{i}">')
        body.append(f'    <rect x="{rx}" y="{y}" width="{rw:.0f}" height="24" rx="8" fill="{fill}" '
                    f'stroke="{stroke}" stroke-width="1" />')
        body.append(f'    <text x="{rx + 8}" y="{y + 17}" font-size="13" font-family="{EMOJI}">{emoji}</text>')
        body.append(f'    <text x="{rx + 26}" y="{y + 16.5}" fill="{TEXT}" font-family="{FONT}" '
                    f'font-size="12" font-weight="600">{count}</text>')
        body.append("  </g>")
        rx += rw + 8
    y += 48

    # typing indicator
    for i in range(3):
        body.append(f'  <circle class="tdot tdot-{i}" cx="{34 + i * 13}" cy="{y}" r="3.5" fill="{MUTED}" />')
    body.append(f'  <text x="74" y="{y + 4}" font-family="{FONT}" font-size="12.5" fill="{MUTED}">'
                f'<tspan font-weight="700" fill="{TEXT}">arnavsao</tspan> is typing the next commit&#8230;</text>')
    H = y + 24

    # ── assemble document ───────────────────────────────────────────
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             f'viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    p.append("  <defs>")
    for idx, cy_ in av_centers.items():
        p.append(f'    <clipPath id="av{idx}"><circle cx="46" cy="{cy_:.0f}" r="20" /></clipPath>')
    p.append("  </defs>")
    p.append("  <style>")
    p.append("    @keyframes slideIn { from { opacity:0; transform:translateX(-16px); } to { opacity:1; transform:translateX(0); } }")
    for i in range(msg + 1):
        p.append(f"    .m{i} {{ opacity:0; animation: slideIn .5s ease-out {0.2 + i * 0.5:.2f}s forwards; }}")
    p.append("    @keyframes popIn { 0% { opacity:0; transform:scale(.5); } 70% { opacity:1; transform:scale(1.1); } 100% { opacity:1; transform:scale(1); } }")
    for i in range(len(STACK)):
        p.append(f"    .chip-{i} {{ opacity:0; transform-origin:center; transform-box:fill-box; "
                 f"animation: popIn .35s ease-out {0.7 + i * 0.07:.2f}s forwards; }}")
    for i in range(len(REACTIONS)):
        p.append(f"    .react-{i} {{ opacity:0; transform-origin:center; transform-box:fill-box; "
                 f"animation: popIn .4s ease-out {2.2 + i * 0.15:.2f}s forwards; }}")
    p.append("    @keyframes edgePulse { 0%,100% { fill:#5865F2; } 50% { fill:#8B5CF6; } }")
    p.append("    .embed-edge { animation: edgePulse 3s ease-in-out infinite; }")
    p.append("    @keyframes bounce { 0%,60%,100% { transform:translateY(0); } 30% { transform:translateY(-6px); } }")
    for i in range(3):
        p.append(f"    .tdot-{i} {{ animation: bounce 1.2s ease-in-out {i * 0.18:.2f}s infinite; }}")
    p.append("    @keyframes hashSpin { 0%,90%,100% { transform:rotate(0deg); } 95% { transform:rotate(12deg); } }")
    p.append("    .hash { transform-origin:center; transform-box:fill-box; animation: hashSpin 5s ease-in-out infinite; }")
    p.append("  </style>")

    p.append(f'  <rect width="{W}" height="{H}" rx="12" fill="{BG}" />')
    p.append(f'  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="11.5" fill="none" stroke="{DIVIDER}" />')

    # channel header bar
    p.append(f'  <path d="M0,12 Q0,0 12,0 L{W - 12},0 Q{W},0 {W},12 L{W},42 L0,42 Z" fill="{HEADER_BG}" />')
    p.append(f'  <line x1="0" y1="42" x2="{W}" y2="42" stroke="{DIVIDER}" stroke-width="1" />')
    p.append(f'  <text class="hash" x="20" y="28" fill="{MUTED}" font-family="{FONT}" font-size="19" '
             f'font-weight="700">#</text>')
    p.append(f'  <text x="38" y="27" fill="{HEADING}" font-family="{FONT}" font-size="15" '
             f'font-weight="700">tech-stack</text>')
    p.append(f'  <line x1="132" y1="12" x2="132" y2="30" stroke="{DIVIDER}" stroke-width="1" />')
    p.append(f'  <text x="144" y="27" fill="{MUTED}" font-family="{FONT}" font-size="12.5">'
             f'tools I ship with — updated daily by a GitHub Action</text>')
    p.append(f'  <circle cx="{W - 96}" cy="21" r="4" fill="{ONLINE}" />')
    p.append(f'  <text x="{W - 86}" y="25" fill="{MUTED}" font-family="{FONT}" font-size="12">1 online</text>')

    p.extend(body)
    p.append("</svg>")

    svg = "\n".join(p)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"✓ Discord chat SVG → {OUTPUT}  ({len(svg)} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
