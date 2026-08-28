#!/usr/bin/env python3
"""
prep_photo.py
─────────────
Remove the background, boost local contrast (CLAHE), and composite
onto pure white so the ASCII ramp maps background → spaces.

Usage:
    python scripts/prep_photo.py [source-photo]   # default: profile_pic.png
Output:
    source-prepped.png
"""

import sys
import pathlib
import numpy as np
from PIL import Image
from rembg import remove
import cv2

ROOT = pathlib.Path(__file__).resolve().parent.parent
INPUT = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "profile_pic.png")
OUTPUT = ROOT / "source-prepped.png"


def main() -> None:
    # ── 1. Remove background ────────────────────────────────────────────
    raw = Image.open(INPUT).convert("RGBA")
    nobg = remove(raw)                                  # transparent BG

    # ── 2. Composite onto white ─────────────────────────────────────────
    white = Image.new("RGBA", nobg.size, (255, 255, 255, 255))
    composite = Image.alpha_composite(white, nobg).convert("L")  # grayscale

    # ── 3. CLAHE (contrast-limited adaptive histogram equalization) ─────
    arr = np.array(composite)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    arr = clahe.apply(arr)

    # ── 4. Save ─────────────────────────────────────────────────────────
    Image.fromarray(arr).save(OUTPUT)
    print(f"✓ Saved prepped photo → {OUTPUT}")


if __name__ == "__main__":
    main()
