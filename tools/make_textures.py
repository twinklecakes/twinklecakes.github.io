"""Generates the dust and book-cloth textures in static/textures/.
Run: python3 tools/make_textures.py   (needs numpy + pillow)
The output PNGs are committed, so you only need this to tweak the look."""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "static" / "textures"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7)


def smooth_noise(h, w, scale, octaves=4):
    """Cheap fractal value noise in [0,1]."""
    total = np.zeros((h, w))
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        s = max(1, int(scale / (2 ** o)))
        small = rng.random((h // s + 2, w // s + 2))
        img = Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        total += amp * np.asarray(img, float) / 255
        norm += amp
        amp *= 0.5
    return total / norm


def dust(W=400, H=400):
    """Transparent PNG of dust specks, fibres and a soft film."""
    a = smooth_noise(H, W, 60) * 70
    specks = rng.random((H, W))
    a += (specks > 0.992) * 160 + (specks > 0.97) * 40
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for _ in range(25):                                             # little fibres
        x, y = rng.integers(0, W), rng.integers(0, H)
        pts = [(x, y)]
        for _ in range(6):
            x += rng.normal(0, 4); y += rng.normal(0, 4); pts.append((x, y))
        d.line(pts, fill=150, width=1)
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = (232, 226, 214)
    rgba[..., 3] = np.asarray(im.filter(ImageFilter.GaussianBlur(0.6)))
    Image.fromarray(rgba, "RGBA").save(OUT / "dust.png", optimize=True)


def cloth(W=256, H=256):
    """Book-cloth weave, grey, meant to be blended over a colour."""
    x = np.arange(W)[None, :]; y = np.arange(H)[:, None]
    weave = (np.sin(x * 1.9) * np.sin(y * 1.9)) * 0.5 + 0.5
    n = smooth_noise(H, W, 20) * 0.6 + rng.random((H, W)) * 0.4
    v = 128 + (weave - 0.5) * 50 + (n - 0.5) * 70
    Image.fromarray(np.clip(v, 0, 255).astype(np.uint8), "L").convert("RGB").save(OUT / "cloth.png", optimize=True)


dust(); cloth()   # (the shelf is Avelyn's plank drawing: tools/make_art.py --shelf)
print("wrote", *sorted(p.name for p in OUT.iterdir()))
