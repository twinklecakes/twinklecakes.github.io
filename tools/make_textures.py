"""Generates the shelf, dust and cloth textures in static/textures/.
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


def wood(h, w, base, dark, light, stretch=60):
    """Wood grain: long wavy stripes along x."""
    y = np.arange(h)[:, None] * np.ones((1, w))
    warp = smooth_noise(h, w, 220) * 40 + smooth_noise(h, w, 30, 2) * 3
    rings = np.sin((y + warp) / h * stretch) * 0.5 + 0.5
    rings = rings ** 3
    fine = smooth_noise(h, w, 6, 2)
    streak = np.asarray(Image.fromarray((rng.random((h, w // 40 + 1)) * 255).astype(np.uint8))
                        .resize((w, h), Image.BILINEAR), float) / 255
    t = 0.55 * rings + 0.25 * fine + 0.2 * streak
    base, dark, light = (np.array(c, float) for c in (base, dark, light))
    col = base + (dark - base) * t[..., None] + (light - base) * (1 - t[..., None]) * 0.35
    return np.clip(col, 0, 255)


def shelf_tile(W=2400, H=560):
    """One shelf row: transparent above, a wooden plank cut out of a 'photo' at the bottom.
    Plank: top face (lit) + front edge + soft shadow, with a scissor-cut white border."""
    top_h, front_h, shadow_h = 34, 58, 26
    plank_h = top_h + front_h
    y0 = H - plank_h - shadow_h
    img = np.zeros((H, W, 4), float)

    top = wood(top_h, W, (176, 128, 82), (112, 70, 38), (220, 180, 130), stretch=25)
    top *= np.linspace(0.85, 1.08, top_h)[:, None, None]          # light from the front
    front = wood(front_h, W, (140, 92, 52), (70, 40, 20), (190, 140, 95), stretch=40)
    front *= np.linspace(1.0, 0.72, front_h)[:, None, None]
    front[:3] = front[:3] * 1.25                                    # bevel highlight
    plank = np.concatenate([top, front], axis=0)

    # dust lying on top surface
    dust = smooth_noise(top_h, W, 40) * 0.25 + (rng.random((top_h, W)) > 0.985) * 0.5
    plank[:top_h] = plank[:top_h] * (1 - dust[..., None] * 0.6) + 225 * dust[..., None] * 0.6

    # scissor-cut mask: wobbly edges, slightly uneven ends
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    pts_top = [(x, y0 + 4 + rng.normal(0, 1.6)) for x in range(10, W - 10, 24)]
    pts_bot = [(x, y0 + plank_h - 2 + rng.normal(0, 1.6)) for x in range(W - 10, 10, -24)]
    d.polygon(pts_top + [(W - 4, y0 + 10), (W - 8, y0 + plank_h - 6)] + pts_bot + [(6, y0 + plank_h - 4), (2, y0 + 8)], fill=255)
    mask_np = np.asarray(mask, float) / 255
    # white paper border around the cut
    border = np.asarray(mask.filter(ImageFilter.MaxFilter(9)), float) / 255
    shadow = np.asarray(mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(10)), float) / 255
    shadow = np.vstack([np.zeros((14, W)), shadow[:-14]])          # shift down, no wrap

    img[..., 3] = shadow * 0.45                                     # shadow (black)
    paper = np.array([250, 248, 242], float)
    img[..., :3] = img[..., :3] * (1 - border[..., None]) + paper * border[..., None]
    img[..., 3] = np.maximum(img[..., 3], border)
    region = np.zeros((H, W, 3))
    region[y0:y0 + plank_h] = plank
    img[..., :3] = img[..., :3] * (1 - mask_np[..., None]) + region * mask_np[..., None]
    img[..., 3] = np.clip(img[..., 3], 0, 1) * 255
    Image.fromarray(img.astype(np.uint8), "RGBA").save(OUT / "shelf.png", optimize=True)


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


dust(); cloth()   # the shelf now comes from Avelyn's plank drawing (tools/make_art.py --shelf)
print("wrote", *sorted(p.name for p in OUT.iterdir()))
