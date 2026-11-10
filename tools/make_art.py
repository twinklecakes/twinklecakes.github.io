"""Turns a drawing on white into a see-through PNG (the paper and pale
highlights become transparent, the colour stays), cropped to the drawing.

    python3 tools/make_art.py DRAWING.jpg OUT.png [--max 1200] [--pad 0.02]
    python3 tools/make_art.py --shelf assets/art/plank.png static/textures/shelf-plank.png

PNGs are written fresh from pixel data: no camera metadata or colour profile.
Needs numpy and pillow.
"""
import argparse
import sys
import numpy as np
from PIL import Image, ImageOps

if len(sys.argv) == 4 and sys.argv[1] == "--shelf":
    # One shelf row for the CSS background: 2400x560, the plank (2400x220) along
    # the bottom. Jars and books stand on its top face, 31% of the row height up.
    plank = Image.open(sys.argv[2]).convert("RGBA").resize((2400, 220), Image.LANCZOS)
    tile = Image.new("RGBA", (2400, 560), (0, 0, 0, 0))
    tile.alpha_composite(plank, (0, 340))
    tile.save(sys.argv[3], optimize=True)
    print(sys.argv[3], tile.size)
    sys.exit()

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--max", type=int, default=1200, help="longest side of the output, px")
ap.add_argument("--pad", type=float, default=0.02)
ap.add_argument("--boost", type=float, default=1.25, help="how much stronger the colour reads")
a = ap.parse_args()

rgb = np.asarray(ImageOps.exif_transpose(Image.open(a.src)).convert("RGB"), float) / 255
al = np.clip((1 - rgb.min(-1) - 0.03) / 0.97, 0, 1)
col = np.clip(1 - (1 - rgb) / np.maximum(al, 1e-4)[..., None], 0, 1)
al = np.clip(al * a.boost, 0, 1)
ys, xs = np.where(al > 0.06)
H, W = al.shape
py, px = int((ys.max() - ys.min()) * a.pad), int((xs.max() - xs.min()) * a.pad)
box = (max(0, xs.min() - px), max(0, ys.min() - py), min(W, xs.max() + px + 1), min(H, ys.max() + py + 1))
img = Image.fromarray((np.dstack([col, al]) * 255).astype(np.uint8), "RGBA").crop(box)
img.thumbnail((a.max, a.max), Image.LANCZOS)
img.save(a.out, optimize=True)
print(a.out, img.size, "crop box in source:", box)

