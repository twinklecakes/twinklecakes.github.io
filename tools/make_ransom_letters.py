"""Turns photos of letters clipped from magazines into the flickering
ransom-note letters on the home page (static/letters/N-a.png and N-b.png).

    python3 tools/make_ransom_letters.py SLOT MODE PHOTO_A PHOTO_B [--thresh 40]

SLOT   1-6 (a v e l y n)
MODE   "scrap"  keep a scissor-cut piece of the paper around the letter
       "shape"  cut along the letter's own outline (for letters on plain white)

Output PNGs are written fresh from pixel data, so no camera metadata (GPS,
dates, device) is carried over. Needs numpy, pillow, scipy.
"""
import argparse
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from scipy import ndimage as ndi

OUT = Path(__file__).resolve().parent.parent / "static" / "letters"
H_OUT = 240                       # px tall (shown at ~half that, so crisp on retina)

ap = argparse.ArgumentParser()
ap.add_argument("slot", type=int)
ap.add_argument("mode", choices=["scrap", "shape"])
ap.add_argument("a")
ap.add_argument("b")
ap.add_argument("--thresh", type=float, default=40)
ap.add_argument("--bright", action="store_true", help="find a light letter on a busy dark page by brightness")
ap.add_argument("--margin", type=float, default=0.10, help="paper around the letter, as a fraction of its size (scrap mode)")
args = ap.parse_args()


def load(path):
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    return np.asarray(im, float)


def letter_mask(rgb):
    """Pixels that differ from the paper colour (taken from the photo's border)."""
    edge = np.concatenate([rgb[:10].reshape(-1, 3), rgb[-10:].reshape(-1, 3),
                           rgb[:, :10].reshape(-1, 3), rgb[:, -10:].reshape(-1, 3)])
    paper = np.median(edge, axis=0)
    m = np.sqrt(((rgb - paper) ** 2).sum(-1)) > args.thresh
    if args.bright:
        m = rgb.mean(-1) > 190
    m = ndi.binary_opening(m, iterations=2)
    lab, n = ndi.label(m)
    if n:                                   # keep the big pieces, drop specks
        sizes = ndi.sum(m, lab, range(1, n + 1))
        m = np.isin(lab, np.where(sizes > sizes.max() * 0.04)[0] + 1)
    return m


def scrap(rgb, seed):
    m = letter_mask(rgb)
    ys, xs = np.where(m)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    r = random.Random(seed)
    my, mx = int((y1 - y0) * args.margin), int((x1 - x0) * args.margin)
    y0, y1 = max(0, y0 - my), min(rgb.shape[0], y1 + my)
    x0, x1 = max(0, x0 - mx), min(rgb.shape[1], x1 + mx)
    crop = Image.fromarray(rgb[y0:y1, x0:x1].astype(np.uint8))
    W, H = crop.size
    j = min(W, H) * 0.035                   # how ragged the scissor cut is
    pts = [(r.uniform(0, j), r.uniform(0, j)), (W * r.uniform(.4, .6), r.uniform(0, j * 1.5)),
           (W - r.uniform(0, j), r.uniform(0, j)), (W - r.uniform(0, j * 1.5), H * r.uniform(.4, .6)),
           (W - r.uniform(0, j), H - r.uniform(0, j)), (W * r.uniform(.4, .6), H - r.uniform(0, j * 1.5)),
           (r.uniform(0, j), H - r.uniform(0, j)), (r.uniform(0, j * 1.5), H * r.uniform(.4, .6))]
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    out = crop.convert("RGBA")
    out.putalpha(mask.filter(ImageFilter.GaussianBlur(1)))
    return out


def shape(rgb):
    m = ndi.binary_closing(letter_mask(rgb), iterations=2)   # no hole-filling: loops (like the l's curl) stay open
    m = ndi.binary_dilation(m, iterations=3)             # a hair of paper edge, like a careful cut
    ys, xs = np.where(m)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    alpha = ndi.gaussian_filter(m[y0:y1, x0:x1].astype(float), 1.0)
    out = np.dstack([rgb[y0:y1, x0:x1], alpha * 255]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


imgs = []
for i, p in enumerate([args.a, args.b]):
    rgb = load(p)
    im = scrap(rgb, args.slot * 10 + i) if args.mode == "scrap" else shape(rgb)
    im = im.resize((round(im.width * H_OUT / im.height), H_OUT), Image.LANCZOS)
    imgs.append(im)

# same canvas for both versions so they flicker in place
W = max(i.width for i in imgs)
for v, im in zip("ab", imgs):
    c = Image.new("RGBA", (W, H_OUT), (0, 0, 0, 0))
    c.paste(im, ((W - im.width) // 2, 0))
    c.save(OUT / f"{args.slot}-{v}.png", optimize=True)     # PNG written from pixels: no metadata
    print(f"{args.slot}-{v}.png  {W}x{H_OUT}")
