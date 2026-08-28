#!/usr/bin/env python3
"""
make_header_svg.py — Sci-Fi Header Banner (Green Theme)
───────────────────────────────────────────────────────
Animated header with:
  • Large "ARNAV SAO" text with RGB-glitch animation
  • "AI Engineer" subtitle with typing cursor
  • Dot grid background pattern
  • Scanline overlay
  • Neon glow effects

Output: header-banner.svg
"""

import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "header-banner.svg"

# ── Design ──────────────────────────────────────────────────────────
SVG_W = 860
SVG_H = 180
BG = "#0d1117"
GREEN_BRIGHT = "#39d353"
GREEN_MID = "#2ea043"
GREEN_DARK = "#006d32"
TEXT_LIGHT = "#c9d1d9"
DIM = "#30363d"

NAME = "ARNAV SAO"
SUBTITLE = "AI Engineer  ·  LLMs  ·  RAG  ·  Agentic AI"
TAGLINE = "// building intelligence into everything"


def main() -> None:
    parts: list[str] = []

    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}"')
    parts.append(f'     width="{SVG_W}" height="{SVG_H}">')
    parts.append("")

    # ── Defs ────────────────────────────────────────────────────────
    parts.append("  <defs>")
    # Glow filter for title
    parts.append('    <filter id="title-glow" x="-10%" y="-10%" width="120%" height="120%">')
    parts.append(f'      <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur" />')
    parts.append(f'      <feFlood flood-color="{GREEN_BRIGHT}" flood-opacity="0.4" result="color" />')
    parts.append('      <feComposite in="color" in2="blur" operator="in" result="glow" />')
    parts.append('      <feMerge>')
    parts.append('        <feMergeNode in="glow" />')
    parts.append('        <feMergeNode in="SourceGraphic" />')
    parts.append('      </feMerge>')
    parts.append('    </filter>')
    # Subtle glow for subtitle
    parts.append('    <filter id="sub-glow" x="-5%" y="-5%" width="110%" height="110%">')
    parts.append(f'      <feGaussianBlur in="SourceGraphic" stdDeviation="1" result="blur" />')
    parts.append(f'      <feFlood flood-color="{GREEN_MID}" flood-opacity="0.3" result="color" />')
    parts.append('      <feComposite in="color" in2="blur" operator="in" result="glow" />')
    parts.append('      <feMerge>')
    parts.append('        <feMergeNode in="glow" />')
    parts.append('        <feMergeNode in="SourceGraphic" />')
    parts.append('      </feMerge>')
    parts.append('    </filter>')
    # Gradient for border line
    parts.append(f'    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="0%">')
    parts.append(f'      <stop offset="0%" stop-color="{GREEN_BRIGHT}" stop-opacity="0" />')
    parts.append(f'      <stop offset="15%" stop-color="{GREEN_BRIGHT}" stop-opacity="1" />')
    parts.append(f'      <stop offset="50%" stop-color="{GREEN_MID}" stop-opacity="1" />')
    parts.append(f'      <stop offset="85%" stop-color="{GREEN_DARK}" stop-opacity="1" />')
    parts.append(f'      <stop offset="100%" stop-color="{GREEN_DARK}" stop-opacity="0" />')
    parts.append(f'    </linearGradient>')
    parts.append("  </defs>")
    parts.append("")

    # ── Background ──────────────────────────────────────────────────
    parts.append(f'  <rect width="{SVG_W}" height="{SVG_H}" fill="{BG}" rx="8" />')
    parts.append("")

    # ── Dot grid pattern ────────────────────────────────────────────
    parts.append('  <g opacity="0.08">')
    for dy in range(0, SVG_H, 20):
        for dx in range(0, SVG_W, 20):
            parts.append(f'    <circle cx="{dx + 10}" cy="{dy + 10}" r="0.8" fill="{GREEN_BRIGHT}" />')
    parts.append('  </g>')
    parts.append("")

    # ── CSS Animations ──────────────────────────────────────────────
    parts.append("  <style>")
    # Glitch effect — RGB shift (kept for sci-fi feel, but colors could be subtle)
    parts.append("    @keyframes glitch {")
    parts.append("      0%, 90%, 100% { transform: translate(0, 0); opacity: 1; }")
    parts.append("      92% { transform: translate(-2px, 1px); opacity: 0.8; }")
    parts.append("      94% { transform: translate(2px, -1px); opacity: 0.9; }")
    parts.append("      96% { transform: translate(-1px, 2px); opacity: 0.7; }")
    parts.append("      98% { transform: translate(1px, 0px); opacity: 1; }")
    parts.append("    }")
    parts.append("    .glitch-text { animation: glitch 4s ease-in-out infinite; }")
    # Red/blue ghost layers
    parts.append("    @keyframes glitch-r {")
    parts.append("      0%, 90%, 100% { transform: translate(0, 0); }")
    parts.append("      93% { transform: translate(3px, -1px); }")
    parts.append("      97% { transform: translate(-2px, 1px); }")
    parts.append("    }")
    parts.append("    @keyframes glitch-b {")
    parts.append("      0%, 90%, 100% { transform: translate(0, 0); }")
    parts.append("      92% { transform: translate(-3px, 1px); }")
    parts.append("      96% { transform: translate(2px, -1px); }")
    parts.append("    }")
    parts.append("    .ghost-r { animation: glitch-r 4s ease-in-out infinite; }")
    parts.append("    .ghost-b { animation: glitch-b 4s ease-in-out infinite; }")
    # Fade in for subtitle
    parts.append("    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }")
    parts.append("    .fade-in { opacity: 0; animation: fadeIn 1s ease-out 0.5s forwards; }")
    parts.append("    .fade-in-late { opacity: 0; animation: fadeIn 1s ease-out 1.2s forwards; }")
    # Cursor blink
    parts.append("    @keyframes blink { 0%,49% { opacity:1 } 50%,100% { opacity:0 } }")
    parts.append("    .cursor-blink { animation: blink 1s step-end infinite; animation-delay: 1.5s; opacity: 0; }")
    # Scanline
    parts.append(f"    @keyframes scanline {{ 0% {{ transform: translateY(-{SVG_H}px) }} 100% {{ transform: translateY({SVG_H}px) }} }}")
    parts.append("    .scanline { animation: scanline 2.5s linear infinite; }")
    # Border glow pulse
    parts.append("    @keyframes glow-pulse { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }")
    parts.append("    .glow-border { animation: glow-pulse 3s ease-in-out infinite; }")
    parts.append("  </style>")
    parts.append("")

    FONT = "'SF Mono', 'Fira Code', 'Cascadia Code', 'Consolas', monospace"

    # ── Title — Glitch effect with RGB ghost layers ─────────────────
    title_y = 75
    # Red ghost (offset) - keep glitch colors slightly different for contrast
    parts.append(f'  <text class="ghost-r" x="{SVG_W // 2}" y="{title_y}" text-anchor="middle"')
    parts.append(f'        font-family="{FONT}" font-size="42" font-weight="bold"')
    parts.append(f'        fill="#ff3366" opacity="0.15" letter-spacing="12">{NAME}</text>')
    # Blue ghost (offset)
    parts.append(f'  <text class="ghost-b" x="{SVG_W // 2}" y="{title_y}" text-anchor="middle"')
    parts.append(f'        font-family="{FONT}" font-size="42" font-weight="bold"')
    parts.append(f'        fill="#3366ff" opacity="0.15" letter-spacing="12">{NAME}</text>')
    # Main title
    parts.append(f'  <text class="glitch-text" x="{SVG_W // 2}" y="{title_y}" text-anchor="middle"')
    parts.append(f'        font-family="{FONT}" font-size="42" font-weight="bold"')
    parts.append(f'        fill="{TEXT_LIGHT}" letter-spacing="12" filter="url(#title-glow)">{NAME}</text>')
    parts.append("")

    # ── Gradient border line ────────────────────────────────────────
    line_y = title_y + 16
    parts.append(f'  <rect class="glow-border" x="80" y="{line_y}" width="{SVG_W - 160}" height="2" rx="1" fill="url(#border-grad)" />')
    parts.append("")

    # ── Subtitle ────────────────────────────────────────────────────
    sub_y = line_y + 30
    parts.append(f'  <text class="fade-in" x="{SVG_W // 2}" y="{sub_y}" text-anchor="middle"')
    parts.append(f'        font-family="{FONT}" font-size="14"')
    parts.append(f'        fill="{GREEN_BRIGHT}" filter="url(#sub-glow)">{SUBTITLE}</text>')

    # ── Tagline with cursor ─────────────────────────────────────────
    tag_y = sub_y + 24
    parts.append(f'  <text class="fade-in-late" x="{SVG_W // 2}" y="{tag_y}" text-anchor="middle"')
    parts.append(f'        font-family="{FONT}" font-size="11"')
    parts.append(f'        fill="{DIM}">{TAGLINE}</text>')

    # Blinking cursor after tagline
    cursor_x = SVG_W // 2 + len(TAGLINE) * 3.3 + 4
    parts.append(f'  <rect class="cursor-blink" x="{cursor_x:.0f}" y="{tag_y - 9}" width="7" height="12" rx="1" fill="{GREEN_MID}" />')
    parts.append("")

    # ── HUD corner accents ──────────────────────────────────────────
    corner_len = 20
    corner_opacity = "0.4"
    # Top-left
    parts.append(f'  <g opacity="{corner_opacity}" class="fade-in">')
    parts.append(f'    <line x1="12" y1="12" x2="{12 + corner_len}" y2="12" stroke="{GREEN_BRIGHT}" stroke-width="1.5" />')
    parts.append(f'    <line x1="12" y1="12" x2="12" y2="{12 + corner_len}" stroke="{GREEN_BRIGHT}" stroke-width="1.5" />')
    # Top-right
    parts.append(f'    <line x1="{SVG_W - 12}" y1="12" x2="{SVG_W - 12 - corner_len}" y2="12" stroke="{GREEN_BRIGHT}" stroke-width="1.5" />')
    parts.append(f'    <line x1="{SVG_W - 12}" y1="12" x2="{SVG_W - 12}" y2="{12 + corner_len}" stroke="{GREEN_BRIGHT}" stroke-width="1.5" />')
    # Bottom-left
    parts.append(f'    <line x1="12" y1="{SVG_H - 12}" x2="{12 + corner_len}" y2="{SVG_H - 12}" stroke="{GREEN_DARK}" stroke-width="1.5" />')
    parts.append(f'    <line x1="12" y1="{SVG_H - 12}" x2="12" y2="{SVG_H - 12 - corner_len}" stroke="{GREEN_DARK}" stroke-width="1.5" />')
    # Bottom-right
    parts.append(f'    <line x1="{SVG_W - 12}" y1="{SVG_H - 12}" x2="{SVG_W - 12 - corner_len}" y2="{SVG_H - 12}" stroke="{GREEN_DARK}" stroke-width="1.5" />')
    parts.append(f'    <line x1="{SVG_W - 12}" y1="{SVG_H - 12}" x2="{SVG_W - 12}" y2="{SVG_H - 12 - corner_len}" stroke="{GREEN_DARK}" stroke-width="1.5" />')
    parts.append(f'  </g>')
    parts.append("")

    # ── CRT Scanline sweep ──────────────────────────────────────────
    parts.append(f'  <rect class="scanline" x="0" y="0" width="{SVG_W}" height="3" fill="{GREEN_BRIGHT}" opacity="0.06" />')

    parts.append("</svg>")

    svg = "\n".join(parts)
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"✓ Header banner SVG → {OUTPUT}  ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
