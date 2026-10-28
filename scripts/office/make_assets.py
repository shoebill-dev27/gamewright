"""Build the virtual office's picture assets: textures (PIL), then the 3D scene drawn as a flat
illustration (Blender: EEVEE cel shading and Freestyle outlines), then lossless WebP.

    python3 scripts/office/make_assets.py [--preview] [--blender PATH]

Blender renders the office from one fixed camera (scripts/office/scene.py), so every layer lines up:
the base picture with every Role idle, one "busy" picture per Role for its own desk, a seat mask per
Role, and layout.json with the screen positions the page overlays its live UI on. The characters
come from make_sprites.py; `--guide` renders the placeholder figures it paints over.
"""

import argparse
import json
import math
import random
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"

# Role looks: colour, hair, eyes, clothes. Shared with scene.py through roles.json.
ROLES = {
    "game-director": dict(
        color="#f5b942",
        hair="#2a2733",
        eyes="#5a3a26",
        style="neat",
        shirt="#2b3a63",
        outfit="blazer",
        inner="#f4f6fa",
        accent="#f5b942",
        skin="#f5c8a8",
        acc="tie",
        mouth="smile",
    ),
    "game-designer": dict(
        color="#34d399",
        hair="#8a5532",
        eyes="#b8742c",
        style="fluffy",
        shirt="#d39a55",
        outfit="cardigan",
        inner="#f3ead6",
        accent="#34d399",
        skin="#f6cbad",
        acc="scarf",
        mouth="open",
    ),
    "technical-director": dict(
        color="#818cf8",
        hair="#1d2030",
        eyes="#56607a",
        style="spiky",
        shirt="#5b4a9a",
        outfit="sweater",
        inner="#e5e7eb",
        accent="#818cf8",
        skin="#eec0a0",
        acc="glasses",
        mouth="flat",
    ),
    "art-director": dict(
        color="#f472b6",
        hair="#f39ac2",
        eyes="#8b4fc9",
        style="long",
        shirt="#a993dd",
        outfit="blouse",
        inner="#fff7f0",
        accent="#f472b6",
        skin="#f7cfb8",
        acc="beret",
        mouth="smile",
    ),
    "gameplay-engineer": dict(
        color="#38bdf8",
        hair="#26324d",
        eyes="#2f7fd1",
        style="messy",
        shirt="#2d64a8",
        outfit="hoodie",
        inner="#38bdf8",
        accent="#38bdf8",
        skin="#efc2a4",
        acc="headphones",
        mouth="smile",
    ),
    "qa": dict(
        color="#f59e0b",
        hair="#3a2a22",
        eyes="#6b4630",
        style="short",
        shirt="#f08a1c",
        outfit="tee",
        inner="#2f3a4f",
        accent="#f59e0b",
        skin="#f1c4a5",
        acc="glasses",
        mouth="flat",
    ),
    "playtester": dict(
        color="#a3e635",
        hair="#6a4430",
        eyes="#3f9b54",
        style="cap",
        shirt="#9aa6b8",
        outfit="hoodie",
        inner="#a3e635",
        accent="#84cc16",
        skin="#f2c6a7",
        acc="cap",
        mouth="open",
    ),
}


def rgb(hex_color, alpha=255):
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(rgb(a)[:3], rgb(b)[:3])) + (
        255,
    )


# --- textures -----------------------------------------------------------------------------------


def face(role, spec, size=1024):
    """The face, drawn for a planar projection across the front of the head (2R square)."""
    s = size * 2  # draw large, then downsample for smooth edges
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    u = s / 2  # one head radius in pixels

    def at(x, z):  # head units (x right, z up) -> pixels
        return u + x * u, u - z * u

    shade = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    cx, cy = at(0, 1.0)
    ImageDraw.Draw(shade).ellipse(
        [cx - 1.15 * u, cy - 0.62 * u, cx + 1.15 * u, cy + 0.62 * u],
        fill=rgb("#d9978a", 150),
    )
    im.alpha_composite(shade.filter(ImageFilter.GaussianBlur(u * 0.07)))
    blush = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blush)
    for sx in (-1, 1):
        cx, cy = at(sx * 0.42, -0.36)
        bd.ellipse(
            [cx - 0.13 * u, cy - 0.06 * u, cx + 0.13 * u, cy + 0.06 * u],
            fill=(255, 120, 130, 120),
        )
    im.alpha_composite(blush.filter(ImageFilter.GaussianBlur(u * 0.03)))
    dark = rgb("#2a1f24")
    iris_top = mix(spec["eyes"], "#000000", 0.45)
    for sx in (-1, 1):
        cx, cy = at(sx * 0.37, -0.1)
        w, h = 0.17 * u, 0.235 * u
        d.ellipse([cx - w, cy - h, cx + w, cy + h], fill=(255, 255, 255, 255))
        # iris: a vertical gradient, darker at the top, with a pupil and two highlights
        iw, ih = w * 0.86, h * 0.92
        grad = Image.new("RGBA", (round(2 * iw), round(2 * ih)))
        gd = ImageDraw.Draw(grad)
        low = mix(spec["eyes"], "#ffffff", 0.3)
        for y in range(grad.height):
            t = y / max(1, grad.height - 1)
            gd.line(
                [0, y, grad.width, y],
                fill=tuple(
                    round(a + (b - a) * t) for a, b in zip(iris_top[:3], low[:3])
                )
                + (255,),
            )
        mask = Image.new("L", grad.size, 0)
        ImageDraw.Draw(mask).ellipse([0, 0, grad.width - 1, grad.height - 1], fill=255)
        im.paste(grad, (round(cx - iw), round(cy - ih)), mask)
        d.ellipse(
            [cx - iw * 0.48, cy - ih * 0.45, cx + iw * 0.48, cy + ih * 0.55],
            fill=mix(spec["eyes"], "#000000", 0.7),
        )
        d.ellipse(
            [
                cx - iw * 0.75 - sx * 0.1 * iw,
                cy - ih * 0.78,
                cx - iw * 0.05 - sx * 0.1 * iw,
                cy - ih * 0.12,
            ],
            fill=(255, 255, 255, 255),
        )
        d.ellipse(
            [cx + iw * 0.2, cy + ih * 0.35, cx + iw * 0.55, cy + ih * 0.62],
            fill=(255, 255, 255, 235),
        )
        # upper lash: a thick arc with an outer flick; lower lash: a short line
        d.arc(
            [cx - w * 1.12, cy - h * 1.08, cx + w * 1.12, cy + h * 1.3],
            start=200,
            end=340,
            fill=dark,
            width=round(0.05 * u),
        )
        fx = cx + sx * w * 1.05
        d.line(
            [fx, cy - h * 0.45, fx + sx * 0.07 * u, cy - h * 0.7],
            fill=dark,
            width=round(0.035 * u),
        )
        d.arc(
            [cx - w * 0.7, cy - h * 0.2, cx + w * 0.7, cy + h * 1.08],
            start=60,
            end=120,
            fill=dark[:3] + (180,),
            width=round(0.014 * u),
        )
        # brow
        bx, by = at(sx * 0.38, 0.24)
        d.arc(
            [bx - 0.17 * u, by - 0.04 * u, bx + 0.17 * u, by + 0.12 * u],
            start=200,
            end=340,
            fill=mix(spec["hair"], "#000000", 0.35),
            width=round(0.03 * u),
        )
    mx, my = at(0, -0.5)
    lip = rgb("#9c4a3c")
    if spec["mouth"] == "open":
        d.chord(
            [mx - 0.09 * u, my - 0.05 * u, mx + 0.09 * u, my + 0.1 * u],
            start=0,
            end=180,
            fill=lip,
        )
        d.chord(
            [mx - 0.06 * u, my + 0.01 * u, mx + 0.06 * u, my + 0.09 * u],
            start=0,
            end=180,
            fill=rgb("#ef8a8a"),
        )
    elif spec["mouth"] == "smile":
        d.arc(
            [mx - 0.1 * u, my - 0.08 * u, mx + 0.1 * u, my + 0.04 * u],
            start=20,
            end=160,
            fill=lip,
            width=round(0.022 * u),
        )
    else:
        d.line([mx - 0.06 * u, my, mx + 0.06 * u, my], fill=lip, width=round(0.022 * u))
    nx, ny = at(0.02, -0.3)
    d.line(
        [nx, ny, nx - 0.02 * u, ny + 0.03 * u],
        fill=rgb("#d9a089"),
        width=round(0.014 * u),
    )
    return im.resize((size, size), Image.LANCZOS)


def screen(kind, accent, w=640, h=400, seed=0):
    rnd = random.Random(seed)
    bg = {"doc": "#eef2f8", "art": "#1b1e2b", "game": "#14281e"}.get(kind, "#0b1427")
    im = Image.new("RGB", (w, h), rgb(bg)[:3])
    d = ImageDraw.Draw(im)
    acc = rgb(accent)[:3]
    d.rectangle(
        [0, 0, w, 22], fill=rgb("#16223b")[:3] if kind != "doc" else (210, 218, 232)
    )
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        d.ellipse([10 + i * 18, 6, 21 + i * 18, 17], fill=rgb(c)[:3])
    if kind == "code":
        for row in range(16):
            y = 32 + row * 22
            d.rectangle([8, y + 4, 30, y + 12], fill=(60, 74, 104))
            x = 44 + rnd.choice((0, 0, 24, 48))
            for _ in range(rnd.randint(2, 5)):
                ln = rnd.randint(30, 120)
                col = rnd.choice(
                    [
                        acc,
                        (198, 120, 221),
                        (152, 195, 121),
                        (229, 192, 123),
                        (97, 175, 239),
                        (171, 178, 191),
                    ]
                )
                d.rounded_rectangle([x, y + 3, x + ln, y + 13], radius=4, fill=col)
                x += ln + 10
                if x > w - 40:
                    break
        d.rectangle([0, 32 + 6 * 22, w, 32 + 7 * 22], outline=acc, width=2)
    elif kind == "kanban":
        for c in range(3):
            x0 = 14 + c * 208
            d.rounded_rectangle([x0, 34, x0 + 196, 60], radius=6, fill=(32, 46, 76))
            d.rounded_rectangle(
                [x0 + 10, 42, x0 + 90, 52],
                radius=4,
                fill=acc if c == 1 else (150, 165, 190),
            )
            for k in range(rnd.randint(2, 4)):
                y0 = 70 + k * 76
                col = rnd.choice(
                    [
                        (52, 211, 153),
                        (56, 189, 248),
                        (245, 158, 11),
                        (244, 114, 182),
                        (129, 140, 248),
                    ]
                )
                d.rounded_rectangle(
                    [x0, y0, x0 + 196, y0 + 66], radius=8, fill=(26, 38, 64)
                )
                d.rectangle([x0, y0, x0 + 6, y0 + 66], fill=col)
                d.rounded_rectangle(
                    [x0 + 16, y0 + 12, x0 + 160, y0 + 22],
                    radius=4,
                    fill=(205, 215, 230),
                )
                d.rounded_rectangle(
                    [x0 + 16, y0 + 32, x0 + 120, y0 + 40],
                    radius=4,
                    fill=(110, 125, 155),
                )
                d.ellipse([x0 + 160, y0 + 40, x0 + 182, y0 + 62], fill=col)
    elif kind == "chart":
        for i in range(9):
            bh = rnd.randint(60, 260)
            d.rounded_rectangle(
                [30 + i * 64, h - 30 - bh, 70 + i * 64, h - 30],
                radius=6,
                fill=acc if i % 3 == 0 else (59, 130, 246),
            )
        pts = [(30 + i * 64 + 20, 120 + rnd.randint(-50, 60)) for i in range(9)]
        d.line(pts, fill=(52, 211, 153), width=5)
        for p in pts:
            d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], fill=(255, 255, 255))
    elif kind == "map":
        cell = 24
        for gx in range(w // cell):
            for gy in range(1, h // cell):
                v = rnd.random()
                col = (
                    (40, 60, 52)
                    if v < 0.55
                    else (70, 98, 72) if v < 0.8 else (34, 44, 70)
                )
                d.rectangle(
                    [gx * cell, gy * cell, gx * cell + cell - 2, gy * cell + cell - 2],
                    fill=col,
                )
        for _ in range(5):
            x0, y0 = rnd.randint(1, 20) * cell, rnd.randint(2, 12) * cell
            d.rectangle(
                [x0, y0, x0 + rnd.randint(3, 6) * cell, y0 + rnd.randint(2, 4) * cell],
                outline=acc,
                width=3,
            )
        d.line(
            [(50, 300), (200, 300), (200, 120), (420, 120), (420, 260), (590, 260)],
            fill=(250, 204, 21),
            width=6,
        )
    elif kind == "graph":
        nodes = [
            (90, 90),
            (300, 70),
            (520, 110),
            (170, 250),
            (400, 240),
            (560, 320),
            (90, 350),
        ]
        for a, b in [(0, 1), (1, 2), (0, 3), (1, 4), (3, 4), (4, 5), (2, 5), (3, 6)]:
            d.line([nodes[a], nodes[b]], fill=(90, 110, 160), width=4)
        for i, (x, y) in enumerate(nodes):
            col = acc if i in (1, 4) else (56, 189, 248) if i % 2 else (52, 211, 153)
            d.rounded_rectangle(
                [x - 54, y - 22, x + 54, y + 22],
                radius=10,
                fill=(24, 36, 62),
                outline=col,
                width=4,
            )
            d.rounded_rectangle(
                [x - 34, y - 5, x + 34, y + 5], radius=4, fill=(200, 210, 230)
            )
    elif kind == "art":
        d.rectangle([20, 34, 430, h - 16], fill=(244, 238, 230))
        d.ellipse(
            [150, 70, 300, 210], fill=(250, 214, 196), outline=(60, 40, 50), width=4
        )
        d.pieslice(
            [130, 50, 320, 230],
            start=180,
            end=360,
            fill=rgb("#f39ac2")[:3],
            outline=(60, 40, 50),
            width=4,
        )
        d.polygon(
            [(170, 210), (280, 210), (320, 370), (130, 370)],
            fill=acc,
            outline=(60, 40, 50),
        )
        for i, c in enumerate(
            (
                "#f472b6",
                "#a78bfa",
                "#38bdf8",
                "#34d399",
                "#fbbf24",
                "#f87171",
                "#ffffff",
                "#1f2937",
            )
        ):
            d.rounded_rectangle(
                [
                    450 + (i % 2) * 86,
                    40 + (i // 2) * 60,
                    524 + (i % 2) * 86,
                    88 + (i // 2) * 60,
                ],
                radius=8,
                fill=rgb(c)[:3],
            )
        for i in range(3):
            d.rounded_rectangle(
                [450, 290 + i * 34, 610, 316 + i * 34], radius=6, fill=(40, 46, 66)
            )
    elif kind == "tests":
        for row in range(10):
            y = 36 + row * 34
            ok = row != 6
            d.rounded_rectangle([14, y, w - 14, y + 28], radius=6, fill=(20, 32, 54))
            col = (52, 211, 153) if ok else (248, 113, 113)
            d.ellipse([22, y + 4, 42, y + 24], fill=col)
            d.rounded_rectangle(
                [56, y + 9, 56 + rnd.randint(150, 380), y + 19],
                radius=4,
                fill=(190, 200, 220),
            )
            d.rounded_rectangle([w - 90, y + 7, w - 24, y + 21], radius=6, fill=col)
    elif kind == "game":
        cell = 32
        for gx in range(w // cell + 1):
            for gy in range(1, h // cell + 1):
                wall = (
                    gx in (0, w // cell)
                    or gy in (1, h // cell)
                    or (gx == 8 and gy != 6)
                    or rnd.random() < 0.06
                )
                col = (
                    (64, 52, 46)
                    if wall
                    else ((96, 130, 80) if (gx + gy) % 2 else (88, 122, 74))
                )
                d.rectangle(
                    [gx * cell, gy * cell, gx * cell + cell - 1, gy * cell + cell - 1],
                    fill=col,
                )
        d.ellipse(
            [5 * cell + 4, 6 * cell + 4, 6 * cell - 4, 7 * cell - 4],
            fill=(255, 210, 120),
        )
        d.ellipse(
            [5 * cell + 10, 6 * cell - 6, 6 * cell - 10, 6 * cell + 14],
            fill=(250, 230, 210),
        )
        for ex, ey, c in (
            (12, 4, (220, 60, 60)),
            (15, 9, (140, 80, 220)),
            (10, 10, (60, 200, 220)),
        ):
            d.polygon(
                [
                    (ex * cell + 16, ey * cell + 4),
                    (ex * cell + 28, ey * cell + 28),
                    (ex * cell + 4, ey * cell + 28),
                ],
                fill=c,
            )
        d.rounded_rectangle([12, h - 54, 230, h - 14], radius=8, fill=(20, 24, 36))
        d.rounded_rectangle([22, h - 42, 180, h - 28], radius=6, fill=(220, 60, 80))
    elif kind == "doc":
        d.rounded_rectangle([40, 40, w - 40, 66], radius=6, fill=acc)
        for row in range(12):
            y = 84 + row * 24
            d.rounded_rectangle(
                [40, y, 40 + rnd.randint(260, 540), y + 10],
                radius=5,
                fill=(120, 132, 158) if row % 4 else (40, 52, 80),
            )
    return im


def board(w=640, h=420, seed=0):
    """A cork board with sticky notes."""
    rnd = random.Random(seed)
    im = Image.new("RGB", (w, h), (178, 132, 86))
    px = im.load()
    for x in range(w):
        for y in range(h):
            n = rnd.randint(-14, 14)
            r, g, b = px[x, y]
            px[x, y] = (r + n, g + n, b + n)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=(110, 78, 50), width=14)
    for i in range(10):
        x, y = 30 + (i % 5) * 120 + rnd.randint(-8, 8), 30 + (
            i // 5
        ) * 190 + rnd.randint(-8, 8)
        col = rnd.choice(
            [
                (255, 236, 120),
                (255, 170, 190),
                (160, 230, 190),
                (150, 205, 255),
                (255, 196, 130),
            ]
        )
        d.rectangle([x + 5, y + 5, x + 100, y + 100], fill=(120, 90, 60))
        d.rectangle([x, y, x + 95, y + 95], fill=col)
        for k in range(3):
            d.line(
                [x + 12, y + 28 + k * 22, x + 80, y + 28 + k * 22],
                fill=(90, 80, 70),
                width=4,
            )
        d.ellipse([x + 40, y - 6, x + 54, y + 8], fill=(220, 40, 60))
    return im


def window(w=512, h=512, seed=0):
    rnd = random.Random(seed)
    im = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line(
            [0, y, w, y], fill=(int(14 + 40 * t), int(26 + 50 * t), int(64 + 70 * t))
        )
    for _ in range(60):
        x, y = rnd.randint(0, w), rnd.randint(0, h // 2)
        d.point((x, y), fill=(220, 230, 255))
    x = 0
    while x < w:
        bw, bh = rnd.randint(40, 90), rnd.randint(140, 360)
        d.rectangle([x, h - bh, x + bw, h], fill=(18, 26, 48))
        for wy in range(h - bh + 10, h - 6, 16):
            for wx in range(x + 6, x + bw - 6, 12):
                if rnd.random() < 0.35:
                    d.rectangle(
                        [wx, wy, wx + 5, wy + 7],
                        fill=rnd.choice(
                            [(255, 214, 140), (150, 210, 255), (255, 240, 200)]
                        ),
                    )
        x += bw + rnd.randint(2, 10)
    return im


def keyboard(w=512, h=160):
    im = Image.new("RGB", (w, h), (30, 34, 46))
    d = ImageDraw.Draw(im)
    for r in range(5):
        for c in range(15):
            x, y = 8 + c * 33, 8 + r * 30
            d.rounded_rectangle([x, y, x + 28, y + 24], radius=4, fill=(212, 218, 230))
    return im


SCREENS = {
    "game-director": ["chart", "kanban", "doc"],
    "game-designer": ["map", "doc", "kanban"],
    "technical-director": ["graph", "code", "chart"],
    "art-director": ["art", "art", "doc"],
    "gameplay-engineer": ["code", "code", "game"],
    "qa": ["tests", "code", "game"],
    "playtester": ["game", "game", "chart"],
}


def make_textures(out):
    out.mkdir(parents=True, exist_ok=True)
    for i, (role, spec) in enumerate(ROLES.items()):
        face(role, spec).save(out / f"face-{role}.png")
        for k, kind in enumerate(SCREENS[role]):
            screen(kind, spec["color"], seed=i * 10 + k).save(
                out / f"screen-{role}-{k}.png"
            )
    board().save(out / "board.png")
    for i in range(3):
        window(seed=i).save(out / f"window-{i}.png")
    keyboard().save(out / "keyboard.png")
    (out / "roles.json").write_text(json.dumps(ROLES, indent=1))


# --- post ---------------------------------------------------------------------------------------


def post(raw):
    """Lossless WebP: flat colours and thin outlines stay crisp."""
    ASSETS.mkdir(exist_ok=True)
    # faces come from the sprites (make_sprites.py use); a face-*.png left in the scratch
    # directory by an older 3D render would otherwise replace them
    names = ["office"] + [f"{k}-{role}" for role in ROLES for k in ("busy", "mask")]
    for name in names:
        if (raw / f"{name}.png").exists():
            Image.open(raw / f"{name}.png").save(
                ASSETS / f"{name}.webp", lossless=True, quality=100, method=6
            )
    layout = json.loads((raw / "layout.json").read_text())
    (ASSETS / "layout.json").write_text(json.dumps(layout, indent=1) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", action="store_true", help="small, fast render")
    ap.add_argument("--blender", default=shutil.which("blender") or "blender")
    ap.add_argument("--work", default=str(HERE / ".build"), help="scratch directory")
    ap.add_argument("--only", default="all", help="all | base | masks | busy")
    ap.add_argument("--no-post", action="store_true")
    ap.add_argument(
        "--guide",
        action="store_true",
        help="render the sprite Roles in 3D into <work>/guide, for make_sprites.py",
    )
    a = ap.parse_args()
    work = Path(a.work)
    tex, raw = work / "tex", work / ("guide" if a.guide else "raw")
    make_textures(tex)
    raw.mkdir(parents=True, exist_ok=True)
    cmd = [
        a.blender,
        "-b",
        "--factory-startup",
        "--python-exit-code",
        "1",
        "-P",
        str(HERE / "scene.py"),
        "--",
        str(tex),
        str(raw),
        a.only,
    ]
    if a.preview:
        cmd.append("preview")
    if a.guide:
        cmd.append("guide")
    subprocess.run(cmd, check=True)
    if not (a.no_post or a.guide):
        post(raw)


if __name__ == "__main__":
    sys.exit(main())
