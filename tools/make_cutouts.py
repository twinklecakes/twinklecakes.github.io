"""Turns scanned engravings into die-cut 'sticker' PNGs for the home-page collage.

    python3 tools/make_cutouts.py SOURCE.jpg OUTPUT.png [--thresh 40] [--crop x0,y0,x1,y1] [--keep 1]

How it works: the paper colour is guessed from the image border; every pixel that
differs enough from it counts as 'ink'. The ink is closed up into solid shapes,
holes are filled, only the biggest shape(s) are kept, then a white scissor-cut
border and a soft shadow are added. Needs numpy, pillow and scipy.
"""
import argparse

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("out")
ap.add_argument("--thresh", type=float, default=40, help="how different from paper a pixel must be")
ap.add_argument("--crop", help="x0,y0,x1,y1 in source pixels, to pick one figure from a plate")
ap.add_argument("--keep", type=int, default=1, help="how many of the largest shapes to keep")
ap.add_argument("--close", type=int, default=6, help="how much to join up fine lines")
ap.add_argument("--border", type=int, default=10, help="white border width (px)")
ap.add_argument("--width", type=int, default=900, help="output width (px)")
a = ap.parse_args()

im = Image.open(a.src).convert("RGB")
if a.crop:
    im = im.crop(tuple(int(v) for v in a.crop.split(",")))
scale = a.width / im.width
im = im.resize((a.width, round(im.height * scale)), Image.LANCZOS)
rgb = np.asarray(im, float)

# paper colour: median of a thin frame around the edge
edge = np.concatenate([rgb[:8].reshape(-1, 3), rgb[-8:].reshape(-1, 3), rgb[:, :8].reshape(-1, 3), rgb[:, -8:].reshape(-1, 3)])
paper = np.median(edge, axis=0)
dist = np.sqrt(((rgb - paper) ** 2).sum(-1))
ink = dist > a.thresh

# join up hatching into solid shapes, fill holes, drop specks
mask = ndi.binary_closing(ink, structure=np.ones((3, 3)), iterations=a.close)
mask = ndi.binary_fill_holes(mask)
mask = ndi.binary_opening(mask, structure=np.ones((3, 3)), iterations=2)
lab, n = ndi.label(mask)
if n:
    sizes = ndi.sum(mask, lab, range(1, n + 1))
    keep = np.argsort(sizes)[::-1][: a.keep] + 1
    mask = np.isin(lab, keep)
mask = ndi.binary_fill_holes(mask)

# crop to the shape plus room for border + shadow
pad = a.border + 30
ys, xs = np.where(mask)
y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
H, W = y1 - y0 + 1 + 2 * pad, x1 - x0 + 1 + 2 * pad
m = np.zeros((H, W), bool); m[pad:pad + y1 - y0 + 1, pad:pad + x1 - x0 + 1] = mask[y0:y1 + 1, x0:x1 + 1]
art = np.zeros((H, W, 3)); art[pad:pad + y1 - y0 + 1, pad:pad + x1 - x0 + 1] = rgb[y0:y1 + 1, x0:x1 + 1]

# soften the cut edge a touch, and make it slightly wobbly like scissors
cut = ndi.binary_dilation(m, iterations=a.border)
rng = np.random.default_rng(3)
wob = ndi.gaussian_filter(rng.random((H, W)), 6) - 0.5
cut = ndi.gaussian_filter(cut.astype(float), 1.2) + wob * 0.9 > 0.5
cut_a = ndi.gaussian_filter(cut.astype(float), 0.7)
m_a = ndi.gaussian_filter(m.astype(float), 0.8)

shadow = ndi.shift(ndi.gaussian_filter(cut.astype(float), 7), (10, 6), order=1) * 0.35

out = np.zeros((H, W, 4))
out[..., :3] = 0  # shadow colour
out[..., 3] = shadow
paper_white = np.array([251, 248, 239.0])
out[..., :3] = out[..., :3] * (1 - cut_a[..., None]) + paper_white * cut_a[..., None]
out[..., 3] = np.maximum(out[..., 3], cut_a)
out[..., :3] = out[..., :3] * (1 - m_a[..., None]) + art * m_a[..., None]
out[..., 3] = np.clip(out[..., 3], 0, 1) * 255
Image.fromarray(out.astype(np.uint8), "RGBA").save(a.out, optimize=True)
print(f"{a.out}: {W}x{H}, paper={paper.round()}")
