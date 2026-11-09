"""Makes the ransom-note letters for the home page name: each letter is cut from
a scrap of 'newspaper', in two nearly identical versions (A and B) that the page
flips between so the letters seem to flicker.

    python3 tools/make_letters.py FONT_DIR

FONT_DIR must contain the .ttf files named in LETTERS below (free Google Fonts:
Abril Fatface, Anton, Alfa Slab One, Rye, Bungee) — they're only needed to
re-generate; the PNGs in static/letters/ are what the site uses.
"""
import math
import random
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
SYS = Path("/usr/share/fonts/truetype")
OUT = Path(__file__).resolve().parent.parent / "static" / "letters"
OUT.mkdir(parents=True, exist_ok=True)

# letter, font file, size, paper colour, ink colour, base tilt (deg)
LETTERS = [
    ("a", FONT_DIR / "AbrilFatface-Regular.ttf", 230, (232, 226, 208), (28, 26, 24), -4),
    ("V", FONT_DIR / "Anton-Regular.ttf", 210, (24, 22, 22), (238, 232, 218), 3),
    ("e", SYS / "liberation/LiberationSerif-BoldItalic.ttf", 230, (236, 205, 198), (40, 18, 20), -2),
    ("L", FONT_DIR / "AlfaSlabOne-Regular.ttf", 170, (196, 38, 46), (246, 238, 227), 5),
    ("y", FONT_DIR / "Rye-Regular.ttf", 190, (233, 214, 160), (40, 30, 20), -6),
    ("N", FONT_DIR / "Bungee-Regular.ttf", 150, (106, 138, 76), (20, 32, 14), 2),
]

WORDS = ("the of and to in is was for on that with as by at from his her it an be "
         "council weather harbour market evening edition notice river sale "
         "season letters said would after new year city first").split()


def paper(w, h, color, seed):
    rng = np.random.default_rng(seed)
    base = np.ones((h, w, 3)) * np.array(color, float)
    base += rng.normal(0, 6, (h, w, 1))                      # grain
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    lum = sum(color) / 3
    faint = tuple(int(c * 0.78) if lum > 110 else min(255, int(c + 40)) for c in color)
    # columns of tiny body text, like the back of a newspaper clipping
    small = ImageFont.truetype(str(SYS / "liberation/LiberationSerif-Regular.ttf"), 13)
    r = random.Random(seed)
    for y in range(-4, h, 15):
        x = -r.randint(0, 40)
        while x < w:
            word = r.choice(WORDS)
            d.text((x, y), word, font=small, fill=faint)
            x += int(d.textlength(word + " ", font=small))
    # halftone dots
    dots = Image.new("L", (w, h), 0)
    dd = ImageDraw.Draw(dots)
    for y in range(0, h, 6):
        for x in range((y // 6) % 2 * 3, w, 6):
            dd.ellipse([x, y, x + 1.6, y + 1.6], fill=40)
    shade = Image.new("RGB", (w, h), (0, 0, 0) if lum > 110 else (255, 255, 255))
    im = Image.composite(shade, im, dots)
    return im


def letter(ch, font_path, size, pcol, ink, tilt, variant, seed):
    font = ImageFont.truetype(str(font_path), size)
    l, t, r_, b = font.getbbox(ch)
    gw, gh = r_ - l, b - t
    rnd = random.Random(seed * 10 + variant)
    pad = 22
    W, H = gw + pad * 2 + 10, gh + pad * 2 + 10
    im = paper(W, H, pcol, seed).convert("RGBA")
    # ink, slightly mottled like cheap printing
    layer = Image.new("L", (W, H), 0)
    dx, dy = rnd.uniform(-2, 2), rnd.uniform(-2, 2)
    ImageDraw.Draw(layer).text((pad + 5 - l + dx, pad + 5 - t + dy), ch, font=font, fill=255)
    mott = np.asarray(layer, float) * (0.82 + 0.18 * np.random.default_rng(seed).random((H, W)))
    layer = Image.fromarray(mott.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5))
    im.paste(Image.new("RGBA", (W, H), ink + (255,)), (0, 0), layer)
    # scissor cut: an uneven polygon just inside the scrap
    cr = random.Random(seed * 7 + variant * 3)
    m = 6
    pts = [(cr.uniform(0, m), cr.uniform(0, m)),
           (W * cr.uniform(0.35, 0.65), cr.uniform(0, m * 1.5)),
           (W - cr.uniform(0, m), cr.uniform(0, m)),
           (W - cr.uniform(0, m * 1.5), H * cr.uniform(0.35, 0.65)),
           (W - cr.uniform(0, m), H - cr.uniform(0, m)),
           (W * cr.uniform(0.35, 0.65), H - cr.uniform(0, m * 1.5)),
           (cr.uniform(0, m), H - cr.uniform(0, m)),
           (cr.uniform(0, m * 1.5), H * cr.uniform(0.35, 0.65))]
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    im.putalpha(mask.filter(ImageFilter.GaussianBlur(0.6)))
    angle = tilt + (0.9 if variant else -0.9) + rnd.uniform(-0.4, 0.4)
    im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    return im


for i, (ch, fp, size, pcol, ink, tilt) in enumerate(LETTERS, 1):
    a = letter(ch, fp, size, pcol, ink, tilt, 0, i)
    b = letter(ch, fp, size, pcol, ink, tilt, 1, i)
    # same canvas size for both versions so they line up
    W, H = max(a.width, b.width), max(a.height, b.height)
    for v, im in (("a", a), ("b", b)):
        c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        c.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
        c = c.resize((W // 2, H // 2), Image.LANCZOS)          # 2x source → crisp on retina
        c.save(OUT / f"{i}-{v}.png", optimize=True)
    print(ch, W // 2, H // 2)
