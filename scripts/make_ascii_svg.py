#!/usr/bin/env python3
"""
make_ascii_svg.py — Sci-Fi Edition
───────────────────────────────────
Convert source-prepped.png into a neon-cyan ASCII-art SVG with:
  • Row-by-row typing animation (SMIL clip wipe)
  • Animated blinking cursor after typing completes
  • CRT scanline sweep (looping)
  • Neon glow text-shadow via SVG filter
  • Deep space background with vignette

Output: avi-ascii.svg
"""

import pathlib
import html
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
INPUT = ROOT / "source-prepped.png"
OUTPUT = ROOT / "avi-ascii.svg"

# ── Tuning ────────────────────────────────────────────────────────────
COLS = 100
ASPECT = 0.55
FONT_SIZE = 6.5
LINE_HEIGHT = 1.15
RAMP = " .`:-=+*cs#%@"

# Animation
ROW_DURATION = 0.08
ROW_STAGGER  = 0.025
CURSOR_WIDTH = 4

# ── Sci-Fi Colors ─────────────────────────────────────────────────────
BG_COLOR     = "#0d1117"
TEXT_COLOR    = "#39d353"
CURSOR_COLOR = "#39d353"
SCANLINE_COLOR = "#39d353"
GLOW_COLOR   = "#39d353"


def brightness_to_char(brightness: float) -> str:
    idx = int((1.0 - brightness / 255.0) * (len(RAMP) - 1))
    idx = max(0, min(len(RAMP) - 1, idx))
    return RAMP[idx]


def main() -> None:
    img = Image.open(INPUT).convert("L")
    w, h = img.size
    rows = int(COLS * (h / w) * ASPECT)
    img = img.resize((COLS, rows), Image.LANCZOS)

    pixels = list(img.getdata())
    grid: list[str] = []
    for r in range(rows):
        line = ""
        for c in range(COLS):
            line += brightness_to_char(pixels[r * COLS + c])
        grid.append(line.rstrip())

    # ── SVG dimensions ──────────────────────────────────────────────
    char_w = FONT_SIZE * 0.6
    char_h = FONT_SIZE * LINE_HEIGHT
    svg_w = COLS * char_w + 20
    svg_h = rows * char_h + 20
    total_type_dur = ROW_STAGGER * rows + ROW_DURATION

    # ── Build SVG ───────────────────────────────────────────────────
    lines: list[str] = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w:.1f} {svg_h:.1f}"')
    lines.append(f'     width="{svg_w:.0f}" height="{svg_h:.0f}">')
    lines.append("")

    # ── Background with vignette ────────────────────────────────────
    lines.append("  <defs>")
    # Vignette gradient
    lines.append('    <radialGradient id="vignette" cx="50%" cy="50%" r="70%">')
    lines.append(f'      <stop offset="0%" stop-color="{BG_COLOR}" stop-opacity="0" />')
    lines.append(f'      <stop offset="100%" stop-color="#000000" stop-opacity="0.6" />')
    lines.append('    </radialGradient>')
    # Neon glow filter
    lines.append('    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">')
    lines.append(f'      <feGaussianBlur in="SourceGraphic" stdDeviation="0.8" result="blur" />')
    lines.append(f'      <feFlood flood-color="{GLOW_COLOR}" flood-opacity="0.3" result="color" />')
    lines.append('      <feComposite in="color" in2="blur" operator="in" result="glow" />')
    lines.append('      <feMerge>')
    lines.append('        <feMergeNode in="glow" />')
    lines.append('        <feMergeNode in="SourceGraphic" />')
    lines.append('      </feMerge>')
    lines.append('    </filter>')

    # Row clip-paths
    for i in range(rows):
        clip_id = f"clip-r{i}"
        y = 10 + i * char_h
        lines.append(f'    <clipPath id="{clip_id}">')
        lines.append(f'      <rect x="0" y="{y:.1f}" width="0" height="{char_h + 1:.1f}">')
        begin = f"{ROW_STAGGER * i:.3f}s"
        lines.append(f'        <animate attributeName="width" from="0" to="{svg_w:.1f}"')
        lines.append(f'                 dur="{ROW_DURATION}s" begin="{begin}" fill="freeze" />')
        lines.append(f'      </rect>')
        lines.append(f'    </clipPath>')
    lines.append("  </defs>")
    lines.append("")

    # Background rect
    lines.append(f'  <rect width="{svg_w:.1f}" height="{svg_h:.1f}" fill="{BG_COLOR}" />')
    lines.append(f'  <rect width="{svg_w:.1f}" height="{svg_h:.1f}" fill="url(#vignette)" />')
    lines.append("")

    # Style
    lines.append("  <style>")
    lines.append(f'    text {{ font-family: "SF Mono", "Fira Code", "Cascadia Code", "Consolas", monospace;')
    lines.append(f"           font-size: {FONT_SIZE}px; fill: {TEXT_COLOR}; }}")
    lines.append(f"    .cursor {{ fill: {CURSOR_COLOR}; }}")
    lines.append(f"    @keyframes blink {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}")
    lines.append(f"    .blink {{ animation: blink 1s step-end infinite; animation-delay: {total_type_dur:.2f}s; opacity:0; }}")
    lines.append(f"    @keyframes scanline {{ 0% {{ transform: translateY(-{svg_h:.0f}px) }} 100% {{ transform: translateY({svg_h:.0f}px) }} }}")
    lines.append(f"    .scanline {{ animation: scanline 3s linear infinite; animation-delay: {total_type_dur:.2f}s; }}")
    lines.append("  </style>")
    lines.append("")

    # Text rows with glow filter
    lines.append('  <g filter="url(#glow)">')
    for i, row_text in enumerate(grid):
        y = 10 + i * char_h + FONT_SIZE
        clip_id = f"clip-r{i}"
        escaped = html.escape(row_text) if row_text else " "
        lines.append(f'    <g clip-path="url(#{clip_id})">')
        lines.append(f'      <text x="10" y="{y:.1f}" xml:space="preserve">{escaped}</text>')
        lines.append(f'    </g>')
    lines.append('  </g>')
    lines.append("")

    # Cursor blocks — ride the wipe edge
    for i in range(rows):
        y = 10 + i * char_h
        begin = f"{ROW_STAGGER * i:.3f}s"
        lines.append(f'  <rect class="cursor" x="0" y="{y:.1f}" width="{CURSOR_WIDTH}" height="{char_h:.1f}" opacity="0">')
        lines.append(f'    <animate attributeName="x" from="10" to="{svg_w - 10:.1f}"')
        lines.append(f'             dur="{ROW_DURATION}s" begin="{begin}" fill="freeze" />')
        lines.append(f'    <animate attributeName="opacity" values="0;0.9;0.9;0" keyTimes="0;0.05;0.9;1"')
        lines.append(f'             dur="{ROW_DURATION}s" begin="{begin}" fill="freeze" />')
        lines.append(f'  </rect>')

    # Blinking cursor at the end of the last row
    last_row_text = grid[-1] if grid else ""
    cursor_x = 10 + len(last_row_text) * char_w + 2
    cursor_y = 10 + (rows - 1) * char_h
    lines.append(f'  <rect class="cursor blink" x="{cursor_x:.1f}" y="{cursor_y:.1f}" width="{CURSOR_WIDTH + 2}" height="{char_h:.1f}" />')
    lines.append("")

    # CRT scanline sweep
    lines.append(f'  <rect class="scanline" x="0" y="0" width="{svg_w:.1f}" height="2" fill="{SCANLINE_COLOR}" opacity="0.08" />')

    lines.append("</svg>")

    svg_content = "\n".join(lines)
    OUTPUT.write_text(svg_content, encoding="utf-8")
    print(f"✓ ASCII SVG → {OUTPUT}  ({rows} rows × {COLS} cols, {len(svg_content)} bytes)")


if __name__ == "__main__":
    main()
