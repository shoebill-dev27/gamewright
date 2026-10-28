"""Paint the Roles' characters into the rendered office as 2D sprites, from the character design
sheet (the canon), with an anime SDXL model guided by the sheet through IP-Adapter.

    python3 scripts/office/make_assets.py --guide && python3 scripts/office/make_assets.py
    ~/.venvs/office-sprites/bin/python scripts/office/make_sprites.py paint <role> [--seeds 1,2,3,4]
    python3 scripts/office/make_sprites.py use <role> <busy seed> <idle seed>

`paint` repaints the placeholder 3D figure of a guide render (.build/guide: it sets the figure's
size, place and pose) around the Role's seat, cuts the figure out and keeps only what the seat
mask shows (the desk stands in front). It needs a CUDA GPU, `diffusers`, `accelerate` and
`rembg`, the SDXL checkpoint and VAE named by OFFICE_SDXL and OFFICE_SDXL_VAE, and the IP-Adapter
weights (downloaded from Hugging Face on first use). Candidates go to .build/sprites/<role>/;
`use` installs the chosen ones as assets/char-<role>-<state>.webp with the agent-card face, so
painting again never replaces an approved picture.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter

HERE = Path(__file__).resolve().parent
SHEET = HERE / "design" / "characters.png"
OUT = HERE / ".build" / "sprites"
RAW, GUIDE = HERE / ".build" / "raw", HERE / ".build" / "guide"

# Each Role: where it stands on the sheet (head to waist; `ref` narrows the reference when a hand
# pose in it would carry over into the picture), a few words for its look, and its expression at
# work and idle (the prompt must stay within the encoder's 77 tokens).
CHARACTERS = {
    "game-director": dict(
        box=(10, 150, 250, 480),
        who="1boy",
        look="black hair, short hair, amber eyes, navy long coat with gold trim, dark vest",
        busy="serious",
        idle="confident smile",
    ),
    "game-designer": dict(
        box=(255, 150, 490, 480),
        ref=(345, 190, 475, 345),  # head and shoulders: the pen hand would carry over
        who="1girl",
        look="brown hair, hair bun, brown eyes, teal jacket, white shirt",
        busy="focused, gentle smile",
        idle="cheerful smile, open mouth",
    ),
    "technical-director": dict(
        box=(490, 150, 735, 480),
        who="1boy",
        look="dark navy hair, glasses, purple eyes, black jacket with purple trim",
        busy="focused, calm",
        idle="calm slight smile",
    ),
    "art-director": dict(
        box=(965, 150, 1205, 480),
        who="1girl",
        look="long pink hair, black beret, pink eyes, white jacket, black and pink outfit",
        busy="concentrating, gentle expression",
        idle="gentle smile, head tilt",
    ),
    "gameplay-engineer": dict(
        box=(745, 150, 965, 480),
        ref=(765, 180, 905, 350),  # head and shoulders: the peace sign would carry over
        who="1girl",
        look=(
            "black cap with cat ears, silver hair with blue tint, blue eyes, "
            "blue headphones, white jacket, light blue hood"
        ),
        busy="looking down at a laptop, typing, focused, closed mouth",
        idle="peace sign, happy, open mouth smile",
    ),
    "qa": dict(
        box=(1205, 150, 1440, 480),
        who="1girl",
        look="short brown bob hair, round glasses, brown eyes, orange and white jacket",
        busy="focused, squinting",
        idle="cheerful smile",
    ),
    "playtester": dict(
        box=(1435, 150, 1672, 480),
        who="1boy",
        look="light brown hair, black cap with green, green eyes, white and lime green jacket",
        busy="excited, open mouth",
        idle="big grin",
    ),
}
PAINT = (
    "{who}, solo, upper body, sitting at a desk behind a laptop, {act}, {pose}, from above, "
    "{look}, anime, clean lineart, vivid colors"
)
ACT = {  # the hands stay out of sight: behind the laptop lid, or in the lap behind the desk
    "busy": "typing, looking down at the laptop",
    "idle": "leaning back, relaxed, looking at viewer, hands out of frame",
}
NEGATIVE = (
    "lowres, bad anatomy, bad hands, extra fingers, blurry, text, watermark, multiple views, "
    "frame, monochrome, pale colors, standing, full body, hairband, chair, raised hand, "
    "peace sign, waving, hand on own face, hand on chin, holding, pointing"
)
AT_WORK = ", looking at viewer"  # busy pictures look at their work
LINE = (27, 34, 54)  # the office's outline colour (scene.py LINE)


def cutter():
    from rembg import new_session

    return new_session("isnet-anime")


def cut(img, session):
    from rembg import remove

    return remove(img, session=session)


def reference(role, session):
    """The Role's figure from the sheet, cut away from the sheet's text and neighbours, on white."""
    c = CHARACTERS[role]
    fig = Image.open(SHEET).convert("RGB").crop(c.get("ref", c["box"]))
    fig = cut(fig, session)
    fig = fig.crop(fig.getchannel("A").getbbox())
    side = max(fig.size) + 16
    sq = Image.new("RGB", (side, side), "white")
    sq.paste(fig, ((side - fig.width) // 2, (side - fig.height) // 2), fig)
    return sq


def context(role, state):
    """The guide render around the Role's seat (its busy layer over it when busy), the seat mask
    in the same frame, and where the sprite box sits in it."""
    lay = json.loads((RAW / "layout.json").read_text())["roles"][role]
    x, y, w, h = lay["sprite"]
    cx0, cy0 = max(0, round(x - w * 0.35)), max(0, round(y - h * 0.12))
    cx1, cy1 = round(x + w * 1.35), round(y + h * 1.12)
    office = Image.open(GUIDE / "office.png").convert("RGBA")
    if state == "busy":  # the busy layer's place comes from the render it belongs to
        guide = json.loads((GUIDE / "layout.json").read_text())["roles"][role]
        busy = Image.open(GUIDE / f"busy-{role}.png").convert("RGBA")
        office.alpha_composite(busy, tuple(guide["busy"][:2]))
    ctx = office.crop((cx0, cy0, cx1, cy1)).convert("RGB")
    mask = Image.new("L", ctx.size, 0)
    mask.paste(
        Image.open(RAW / f"mask-{role}.png").getchannel("A"),
        (round(x) - cx0, round(y) - cy0),
    )
    return ctx, mask, (round(x) - cx0, round(y) - cy0, round(w), round(h))


def paint(role, states, seeds, scale, strength):
    """Every picture in a process of its own: the pipeline's memory grows from one picture to the
    next until the system kills it."""
    out = OUT / role
    out.mkdir(parents=True, exist_ok=True)
    session = cutter()
    reference(role, session).save(out / "reference.png")
    for state in states:
        for seed in seeds:
            args = ["paint-one", role, state, str(seed), str(scale), str(strength)]
            subprocess.run([sys.executable, __file__, *args], check=True)
            cutout(role, state, seed, session)


def paint_one(role, state, seed, scale, strength):
    import torch
    from diffusers import AutoencoderKL, StableDiffusionXLInpaintPipeline

    out = OUT / role
    ctx, mask, _ = context(role, state)
    k = 1152 / max(ctx.size)
    size = (round(ctx.width * k / 8) * 8, round(ctx.height * k / 8) * 8)
    ctx = ctx.resize(size, Image.LANCZOS)
    mask = mask.resize(size, Image.LANCZOS).filter(ImageFilter.MaxFilter(15))
    vae = AutoencoderKL.from_single_file(
        os.environ["OFFICE_SDXL_VAE"], torch_dtype=torch.float16
    )
    pipe = StableDiffusionXLInpaintPipeline.from_single_file(
        os.environ["OFFICE_SDXL"], vae=vae, torch_dtype=torch.float16
    )
    pipe.load_ip_adapter(
        "h94/IP-Adapter",
        subfolder="sdxl_models",
        weight_name="ip-adapter-plus_sdxl_vit-h.safetensors",
        image_encoder_folder="models/image_encoder",
    )
    pipe.set_ip_adapter_scale(scale)
    pipe.enable_model_cpu_offload()  # fits next to other GPU users
    c = CHARACTERS[role]
    prompt = PAINT.format(who=c["who"], act=ACT[state], pose=c[state], look=c["look"])
    negative = NEGATIVE + (AT_WORK if state == "busy" else "")
    for text in (prompt, negative):  # the encoder silently drops what is past 77 tokens
        n = len(pipe.tokenizer(text).input_ids)
        assert n <= 77, f"{text[:40]}... is {n} tokens; the encoder reads 77"
    img = pipe(
        prompt=prompt,
        negative_prompt=negative,
        image=ctx,
        mask_image=mask,
        ip_adapter_image=Image.open(out / "reference.png"),
        width=size[0],
        height=size[1],
        strength=strength,
        num_inference_steps=32,
        guidance_scale=6.0,
        generator=torch.Generator("cpu").manual_seed(seed),
    ).images[0]
    img.save(out / f"paint-{state}-{seed}-raw.png")
    print("painted", out / f"paint-{state}-{seed}-raw.png", flush=True)


def cutout(role, state, seed, session):
    """The painted figure alone, where the seat shows, in the sprite box at twice its size."""
    out = OUT / role
    ctx, mask, (sx, sy, sw, sh) = context(role, state)
    big = Image.open(out / f"paint-{state}-{seed}-raw.png")
    k = big.width / ctx.width
    # only the solid figure: drop the faint halo of painted background around it, and any
    # stray piece apart from the figure itself (bits of chair, a hand of the guide)
    figure = cut(big, session).getchannel("A").point(lambda v: 0 if v < 96 else v)
    figure = largest_piece(figure)
    # a slightly soft seat edge, so a figure cut by the board's outline or the desk ends gently
    seat = mask.resize(big.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(2.5))
    alpha = ImageChops.darker(figure, seat)  # the figure, where the seat shows
    sprite = big.convert("RGBA")
    sprite.putalpha(alpha)
    box = [round(v * k) for v in (sx, sy, sx + sw, sy + sh)]
    sprite = sprite.crop(box).resize((sw * 2, sh * 2), Image.LANCZOS)
    finish(sprite).save(out / f"paint-{state}-{seed}.png")
    print("cut", out / f"paint-{state}-{seed}.png", flush=True)


def largest_piece(alpha):
    import cv2
    import numpy as np

    a = np.asarray(alpha)
    n, labels, stats, _ = cv2.connectedComponentsWithStats((a > 0).astype(np.uint8))
    if n <= 2:
        return alpha
    keep = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    return Image.fromarray(np.where(labels == keep, a, 0).astype(np.uint8))


def finish(sprite):
    """Match the office: a little more contrast and colour, and the same dark outline the
    renderer draws (about 2 px at display size) around the figure."""
    alpha = sprite.getchannel("A")
    rgb = ImageEnhance.Contrast(sprite.convert("RGB")).enhance(1.12)
    rgb = ImageEnhance.Color(rgb).enhance(1.15)
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    out = Image.new("RGBA", sprite.size, LINE + (0,))
    out.putalpha(alpha.filter(ImageFilter.MaxFilter(9)))  # ~1.5 px at 1920 wide
    body = rgb.convert("RGBA")
    body.putalpha(alpha)
    out.alpha_composite(body)
    return out


def use(role, busy, idle):
    """Install the chosen candidates as the Role's sprites, and its agent-card face from the idle
    one (a square around the head, at the top of the figure)."""
    out = OUT / role
    for state, seed in (("busy", busy), ("idle", idle)):
        # painted shading compresses well; lossy at 94 looks the same and is a fifth of the size
        Image.open(out / f"paint-{state}-{seed}.png").save(
            HERE / "assets" / f"char-{role}-{state}.webp",
            quality=94,
            method=6,
            alpha_quality=100,
        )
    fig = Image.open(out / f"paint-idle-{idle}.png")
    x0, y0, x1, _ = fig.getchannel("A").point(lambda v: 255 if v > 64 else 0).getbbox()
    side, cx = round((x1 - x0) * 0.62), (x0 + x1) / 2
    face = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    face.alpha_composite(
        fig.crop((round(cx - side / 2), y0, round(cx + side / 2), y0 + side))
    )
    face.resize((256, 256), Image.LANCZOS).save(
        HERE / "assets" / f"face-{role}.webp", lossless=True, quality=100
    )
    print("installed", role, busy, idle)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("paint")
    q.add_argument("role", choices=sorted(CHARACTERS))
    q.add_argument("--seeds", default="1,2,3,4")
    q.add_argument("--states", default="busy,idle")
    q.add_argument("--scale", type=float, default=0.6, help="IP-Adapter strength")
    q.add_argument("--strength", type=float, default=0.86, help="how much is repainted")
    o = sub.add_parser("paint-one")
    for name in ("role", "state"):
        o.add_argument(name)
    o.add_argument("seed", type=int)
    o.add_argument("scale", type=float)
    o.add_argument("strength", type=float)
    r = sub.add_parser("recut")
    r.add_argument("role")
    r.add_argument("--seeds", default="1,2,3,4")
    r.add_argument("--states", default="busy,idle")
    u = sub.add_parser("use")
    u.add_argument("role")
    u.add_argument("busy", type=int, help="seed of the chosen busy picture")
    u.add_argument("idle", type=int, help="seed of the chosen idle picture")
    a = ap.parse_args()
    if a.cmd == "paint":
        seeds = [int(s) for s in a.seeds.split(",")]
        return paint(a.role, a.states.split(","), seeds, a.scale, a.strength)
    if a.cmd == "paint-one":
        return paint_one(a.role, a.state, a.seed, a.scale, a.strength)
    if a.cmd == "recut":
        session = cutter()
        for state in a.states.split(","):
            for seed in a.seeds.split(","):
                cutout(a.role, state, int(seed), session)
        return
    return use(a.role, a.busy, a.idle)


if __name__ == "__main__":
    main()
