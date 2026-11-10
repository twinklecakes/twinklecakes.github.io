"""Turns Avelyn's drawings (on white) into the PNGs the site uses. The white
paper and pale highlights become transparent and the colour stays; the result
is cropped to the drawing. PNGs are written fresh from pixel data, so no camera
metadata or colour profile is carried over. Needs numpy, pillow and scipy.

    python3 tools/make_art.py DRAWING.jpg OUT.png [--max 1200] [--pad 0.02] [--boost 1.25]

Extra modes, for the pieces that need more than a plain cut-out:

    --square 220   centre the drawing in a square this many px wide (bubbles)
    --trim         solid fill with a cream cut-out border (the lid on the spill)
    --shelf        build the shelf row tile from the plank drawing

What was made with what:
    assets/art/jar.png            --max 900
    assets/art/jar-tipped.png     --max 1200
    assets/art/lid-trim.png       --max 500 --trim
    assets/art/name.png, name-red.png, title-*.png   --max 1000 / 1100 --boost 1.0
    assets/bubbles/1-5.png        --square 220 --boost 1.35
    static/textures/shelf-plank.png   --shelf --pad 0
"""
import argparse

import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage as ndi

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("out")
ap.add_argument("--max", type=int, default=1200, help="longest side of the output, px")
ap.add_argument("--pad", type=float, default=0.02, help="room around the drawing, as a fraction of its size")
ap.add_argument("--boost", type=float, default=1.25, help="how much stronger the colour reads")
ap.add_argument("--square", type=int, help="centre in a square of this size (px)")
ap.add_argument("--trim", action="store_true", help="solid fill + cream cut-out border")
ap.add_argument("--shelf", action="store_true", help="make the 2400x560 shelf row tile")
a = ap.parse_args()

# --- lift the paper out ---------------------------------------------------
rgb = np.asarray(ImageOps.exif_transpose(Image.open(a.src)).convert("RGB"), float) / 255
al = np.clip((1 - rgb.min(-1) - 0.03) / 0.97, 0, 1)            # how far from white
col = np.clip(1 - (1 - rgb) / np.maximum(al, 1e-4)[..., None], 0, 1)  # colour as if on nothing
al = np.clip(al * a.boost, 0, 1)

# --- crop to the drawing --------------------------------------------------
ys, xs = np.where(al > 0.06)
H, W = al.shape
py, px = int((ys.max() - ys.min()) * a.pad), int((xs.max() - xs.min()) * a.pad)
if a.square:                                                    # square crop around the centre
    cy, cx = (ys.min() + ys.max()) / 2, (xs.min() + xs.max()) / 2
    r = max(ys.max() - ys.min(), xs.max() - xs.min()) / 2 * (1 + 2 * a.pad)
    box = tuple(int(v) for v in (cx - r, cy - r, cx + r, cy + r))
else:
    box = (max(0, xs.min() - px), max(0, ys.min() - py), min(W, xs.max() + px + 1), min(H, ys.max() + py + 1))
img = Image.fromarray((np.dstack([col, al]) * 255).astype(np.uint8), "RGBA").crop(box)

if a.square:
    img = img.resize((a.square, a.square), Image.LANCZOS)
elif a.shelf:
    # one shelf row for the CSS background: the plank (2400x220) along the bottom
    # of a 2400x560 tile; jars and books stand on its top face, 31% of the row up
    plank = img.resize((2400, 220), Image.LANCZOS)
    img = Image.new("RGBA", (2400, 560), (0, 0, 0, 0))
    img.alpha_composite(plank, (0, 340))
else:
    img.thumbnail((a.max, a.max), Image.LANCZOS)

if a.trim:
    # fill the drawing's silhouette solid (art over white) and add a cream
    # scissor-cut border, so it reads as a sticker on top of busy things
    p = 24
    A = np.zeros((img.height + 2 * p, img.width + 2 * p, 4))
    A[p:-p, p:-p] = np.asarray(img, float) / 255
    alpha = A[..., 3]
    m = ndi.binary_opening(ndi.binary_fill_holes(ndi.binary_closing(alpha > 0.05, iterations=6)), iterations=2)
    art = A[..., :3] * alpha[..., None] + (1 - alpha[..., None])
    border = ndi.gaussian_filter(ndi.binary_dilation(m, iterations=9).astype(float), 0.8)
    m_a = ndi.gaussian_filter(m.astype(float), 0.7)[..., None]
    out = np.array([0.984, 0.973, 0.937]) * (1 - m_a) + art * m_a
    img = Image.fromarray((np.dstack([out, border]) * 255).astype(np.uint8), "RGBA")

img.save(a.out, optimize=True)
print(a.out, img.size)
