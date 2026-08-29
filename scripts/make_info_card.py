#!/usr/bin/env python3
"""
make_info_card.py — Sci-Fi HUD Edition
───────────────────────────────────────
Generate a neofetch-style SVG info card with:
  • HUD-style glowing border with corner accents
  • Neon cyan keys, light gray values
  • Staggered fade+slide animation per line
  • Blinking cursor after last line
  • CRT scanline overlay
  • Real AI engineer content

Set STATIC=1 to emit a frozen frame.

Output: info-card.svg
"""

import html
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "info-card.svg"
STATIC = os.environ.get("STATIC", "0") == "1"

# ── Content ─────────────────────────────────────────────────────────
USERNAME = "arnavsao"
HOST     = "neural"
TITLE    = f"{USERNAME}@{HOST}"
SEP      = "─" * len(TITLE)

INFO_LINES = [
    ("Role",       "AI Engineer"),
    ("Focus",      "LLMs · RAG · Agentic AI · Fine-tuning"),
    ("Stack",      "Python · TypeScript · Angular · LangChain"),
    ("Now",        "AI-powered CAD system @ Aagento AI"),
    ("",           "→ NL commands · DXF parsing · Canvas 2D"),
    ("Shipped",    "LLaMA 2 QLoRA fine-tuning (Modal A100)"),
    ("",           "→ Kerala Ayurveda RAG (4-agent pipeline)"),
    ("",           "→ DPR Validator (RAG + OCR, Railways)"),
    ("AI",         "PEFT/LoRA · ChromaDB · Ollama · Gemini"),
    ("",           ""),
    ("Web",        "arnavsao-portfolio.vercel.app"),
]

# ── Sci-Fi Design ───────────────────────────────────────────────────
BG           = "#0d1117"
BORDER       = "#2ea043"
TITLE_COLOR  = "#39d353"
SEP_COLOR    = "#30363d"
KEY_COLOR    = "#39d353"
VAL_COLOR    = "#c9d1d9"
ACCENT_DOTS  = ["#39d353", "#2ea043", "#006d32", "#39d353", "#2ea043", "#006d32"]
PURPLE       = "#2ea043"
MAGENTA      = "#006d32"
CYAN         = "#39d353"

FONT_FAMILY  = "'SF Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace"
FONT_SIZE    = 13
LINE_HEIGHT  = 22
PAD_X        = 28
PAD_Y        = 28

STAGGER      = 0.14
SLIDE_DIST   = 15
FADE_DUR     = 0.45


def main() -> None:
    total_lines = 2 + len(INFO_LINES) + 2  # title + sep + info + blank + dots
    svg_w = 490
    svg_h = PAD_Y * 2 + total_lines * LINE_HEIGHT + 16

    parts: list[str] = []

    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}"')
    parts.append(f'     width="{svg_w}" height="{svg_h}">')
    parts.append("")

    # ── Defs ────────────────────────────────────────────────────────
    parts.append("  <defs>")
    # Glow filter
    parts.append('    <filter id="text-glow" x="-10%" y="-10%" width="120%" height="120%">')
    parts.append(f'      <feGaussianBlur in="SourceGraphic" stdDeviation="0.6" result="blur" />')
    parts.append(f'      <feFlood flood-color="{CYAN}" flood-opacity="0.25" result="color" />')
    parts.append('      <feComposite in="color" in2="blur" operator="in" result="glow" />')
    parts.append('      <feMerge>')
    parts.append('        <feMergeNode in="glow" />')
    parts.append('        <feMergeNode in="SourceGraphic" />')
    parts.append('      </feMerge>')
    parts.append('    </filter>')
    # Border gradient
    parts.append(f'    <linearGradient id="border-g" x1="0%" y1="0%" x2="100%" y2="100%">')
    parts.append(f'      <stop offset="0%" stop-color="{CYAN}" stop-opacity="0.5" />')
    parts.append(f'      <stop offset="50%" stop-color="{PURPLE}" stop-opacity="0.3" />')
    parts.append(f'      <stop offset="100%" stop-color="{MAGENTA}" stop-opacity="0.5" />')
    parts.append(f'    </linearGradient>')
    parts.append("  </defs>")
    parts.append("")

    # Background with glowing border
    parts.append(f'  <rect width="{svg_w}" height="{svg_h}" fill="{BG}" rx="8" />')
    parts.append(f'  <rect x="1" y="1" width="{svg_w - 2}" height="{svg_h - 2}" fill="none" stroke="url(#border-g)" stroke-width="1" rx="7" />')
    parts.append("")

    # ── HUD corner accents ──────────────────────────────────────────
    cl = 14  # corner length
    parts.append(f'  <g opacity="0.5">')
    parts.append(f'    <line x1="6" y1="6" x2="{6+cl}" y2="6" stroke="{CYAN}" stroke-width="1.5" />')
    parts.append(f'    <line x1="6" y1="6" x2="6" y2="{6+cl}" stroke="{CYAN}" stroke-width="1.5" />')
    parts.append(f'    <line x1="{svg_w-6}" y1="6" x2="{svg_w-6-cl}" y2="6" stroke="{CYAN}" stroke-width="1.5" />')
    parts.append(f'    <line x1="{svg_w-6}" y1="6" x2="{svg_w-6}" y2="{6+cl}" stroke="{CYAN}" stroke-width="1.5" />')
    parts.append(f'    <line x1="6" y1="{svg_h-6}" x2="{6+cl}" y2="{svg_h-6}" stroke="{MAGENTA}" stroke-width="1.5" />')
    parts.append(f'    <line x1="6" y1="{svg_h-6}" x2="6" y2="{svg_h-6-cl}" stroke="{MAGENTA}" stroke-width="1.5" />')
    parts.append(f'    <line x1="{svg_w-6}" y1="{svg_h-6}" x2="{svg_w-6-cl}" y2="{svg_h-6}" stroke="{MAGENTA}" stroke-width="1.5" />')
    parts.append(f'    <line x1="{svg_w-6}" y1="{svg_h-6}" x2="{svg_w-6}" y2="{svg_h-6-cl}" stroke="{MAGENTA}" stroke-width="1.5" />')
    parts.append(f'  </g>')
    parts.append("")

    # ── CSS animation ───────────────────────────────────────────────
    total_anim = STAGGER * total_lines + FADE_DUR
    parts.append("  <style>")
    if not STATIC:
        parts.append("    @keyframes fadeSlideIn {")
        parts.append(f"      from {{ opacity: 0; transform: translateX({SLIDE_DIST}px); }}")
        parts.append(f"      to   {{ opacity: 1; transform: translateX(0); }}")
        parts.append("    }")
        for i in range(total_lines):
            delay = STAGGER * i
            parts.append(f"    .line-{i} {{ opacity: 0; animation: fadeSlideIn {FADE_DUR}s ease-out {delay:.2f}s forwards; }}")
    parts.append(f"    @keyframes blink {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}")
    parts.append(f"    .cursor-blink {{ animation: blink 1s step-end infinite; animation-delay: {total_anim:.1f}s; opacity: 0; }}")
    parts.append(f"    @keyframes scanline {{ 0% {{ transform: translateY(-{svg_h}px) }} 100% {{ transform: translateY({svg_h}px) }} }}")
    parts.append(f"    .scanline {{ animation: scanline 3s linear infinite; }}")
    parts.append("  </style>")
    parts.append("")

    # ── Render lines ────────────────────────────────────────────────
    line_idx = 0

    def next_y() -> float:
        nonlocal line_idx
        return PAD_Y + line_idx * LINE_HEIGHT + FONT_SIZE

    def cls() -> str:
        return f"line-{line_idx}" if not STATIC else ""

    # Title
    y = next_y()
    c = cls()
    c_attr = f' class="{c}"' if c else ""
    parts.append(f'  <text x="{PAD_X}" y="{y:.0f}" fill="{TITLE_COLOR}" '
                 f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}" font-weight="bold"'
                 f'{c_attr} filter="url(#text-glow)">{html.escape(TITLE)}</text>')
    line_idx += 1

    # Separator
    y = next_y()
    c = cls()
    c_attr = f' class="{c}"' if c else ""
    parts.append(f'  <text x="{PAD_X}" y="{y:.0f}" fill="{SEP_COLOR}" '
                 f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}"{c_attr}>{SEP}</text>')
    line_idx += 1

    # Info rows
    for key, val in INFO_LINES:
        y = next_y()
        c = cls()
        c_attr = f' class="{c}"' if c else ""
        if key:
            parts.append(
                f'  <text y="{y:.0f}" font-family="{FONT_FAMILY}" '
                f'font-size="{FONT_SIZE}"{c_attr}>'
                f'<tspan x="{PAD_X}" fill="{KEY_COLOR}" font-weight="bold">{html.escape(key)}</tspan>'
                f'<tspan fill="{VAL_COLOR}">  {html.escape(val)}</tspan>'
                f'</text>'
            )
        elif val:
            parts.append(f'  <text x="{PAD_X}" y="{y:.0f}" fill="{VAL_COLOR}" '
                         f'font-family="{FONT_FAMILY}" font-size="{FONT_SIZE}"{c_attr}>'
                         f'  {html.escape(val)}</text>')
        line_idx += 1

    # Blank line
    line_idx += 1

    # Accent color dots
    y = next_y()
    c = cls()
    c_attr = f' class="{c}"' if c else ""
    parts.append(f'  <g{c_attr}>')
    for j, color in enumerate(ACCENT_DOTS):
        cx = PAD_X + j * 22 + 8
        parts.append(f'    <rect x="{cx}" y="{y - 10:.0f}" width="16" height="16" rx="3" fill="{color}" />')
    parts.append("  </g>")
    line_idx += 1

    # ── Blinking cursor ─────────────────────────────────────────────
    # Place it after the last visible info line
    last_info = INFO_LINES[-1]
    last_text = last_info[1] if last_info[1] else last_info[0]
    cursor_line = 2 + len(INFO_LINES) - 1  # last info row index
    cursor_y_pos = PAD_Y + cursor_line * LINE_HEIGHT + 4
    cursor_x_pos = PAD_X + (len(last_info[0]) + 2 + len(last_text)) * 7.8 + 6 if last_info[0] else PAD_X + len(last_text) * 7.8 + 16
    cursor_x_pos = min(cursor_x_pos, svg_w - 40)
    parts.append(f'  <rect class="cursor-blink" x="{cursor_x_pos:.0f}" y="{cursor_y_pos:.0f}" width="8" height="{FONT_SIZE + 2}" rx="1" fill="{PURPLE}" />')
    parts.append("")

    # ── CRT Scanline sweep ──────────────────────────────────────────
    parts.append(f'  <rect class="scanline" x="0" y="0" width="{svg_w}" height="2" fill="{CYAN}" opacity="0.05" />')

    parts.append("</svg>")

    svg = "\n".join(parts)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"✓ Info card SVG → {OUTPUT}  ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
