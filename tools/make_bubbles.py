"""Turns hand-drawn bubbles (on white paper) into see-through bubble PNGs for
the site's bubble effect: assets/bubbles/1.png, 2.png, ...

    python3 tools/make_bubbles.py DRAWING.jpg [DRAWING2.jpg ...]

White is "unmixed" out of every pixel, so the paper disappears and pale
areas (highlights, the clear film) become partly transparent, while the
coloured pencil stays. PNGs are written fresh from pixel data, so no camera
metadata or colour profile is carried over. Needs numpy and pillow.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

OUT = Path(__file__).resolve().parent.parent / "assets" / "bubbles"
OUT.mkdir(parents=True, exist_ok=True)
SIZE = 220          # px; bubbles show at up to ~80px, so this is crisp on retina

for n, path in enumerate(sys.argv[1:], 1):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    rgb = np.asarray(im, float) / 255

    # paper -> transparent: alpha is how far the darkest channel is from white
    a = 1 - rgb.min(-1)
    a = np.clip((a - 0.03) / 0.97, 0, 1)             # ignore faint paper grain
    safe = np.maximum(a, 1e-4)[..., None]
    col = np.clip(1 - (1 - rgb) / safe, 0, 1)        # colour as if laid on nothing
    a = np.clip(a * 1.35, 0, 1)                       # pencil reads a touch stronger on screen

    # crop to the bubble, square, with a little room
    ys, xs = np.where(a > 0.08)
    cy, cx = (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2
    r = max(ys.max() - ys.min(), xs.max() - xs.min()) / 2 * 1.04
    box = tuple(int(v) for v in (cx - r, cy - r, cx + r, cy + r))
    out = np.dstack([col, a])
    img = Image.fromarray((out * 255).astype(np.uint8), "RGBA").crop(box).resize((SIZE, SIZE), Image.LANCZOS)
    img.save(OUT / f"{n}.png", optimize=True)
    print(f"{n}.png  from {Path(path).name}")
