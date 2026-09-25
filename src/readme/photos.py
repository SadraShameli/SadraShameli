"""`uv run readme photos`: crop and resize the photos into the exact frames the cards use.

Only needed after adding or changing a photo. It needs Pillow, which is in the dev
dependency group; drawing the cards needs nothing beyond the standard library.
"""

from .paths import CARD_IMAGES, ROOT

SCALE = 1.5  # retina-ish without bloating the SVGs

# name: (source, frame w, frame h, focus x, focus y)  focus = 0..1 in the source
JOBS = {
    "sensorhub": ("Images/SensorHub1.jpg", 400, 320, 0.5, 0.58),
    "projectai": ("Images/ProjectAI.jpg", 400, 320, 0.52, 0.55),
    # website screenshots, shown inset in a frame (16:10, the whole 1440x900 capture)
    "shot-sadra-nl": ("Images/Screenshots/sadra-nl.jpg", 418, 261, 0.5, 0.0),
    "shot-prop-calculator": ("Images/Screenshots/prop-calculator.jpg", 418, 261, 0.5, 0.0),
    "shot-minomarkt-nl": ("Images/Screenshots/minomarkt-nl.jpg", 418, 261, 0.5, 0.0),
    # the early-lab robot, framed the same way
    "shot-robot": ("Images/Robot.jpg", 418, 261, 0.5, 0.5),
    # YouTube thumbnails: the videos are vertical, so keep the 9:16 middle
    "yt-line-detection": ("Images/YouTube/1142rRZ3rzc.jpg", 126, 224, 0.5, 0.5),
    "yt-lidar-ranging": ("Images/YouTube/_C8PnLK2SWA.jpg", 126, 224, 0.5, 0.5),
    "yt-indoor-test": ("Images/YouTube/abyVlfAETG0.jpg", 126, 224, 0.5, 0.5),
}


def crop_box(src_w: int, src_h: int, w: int, h: int, fx: float, fy: float) -> tuple[int, int, int, int]:
    aspect = w / h
    if src_w / src_h > aspect:
        ch, cw = src_h, round(src_h * aspect)
    else:
        cw, ch = src_w, round(src_w / aspect)
    left = min(max(round(fx * src_w - cw / 2), 0), src_w - cw)
    top = min(max(round(fy * src_h - ch / 2), 0), src_h - ch)
    return left, top, left + cw, top + ch


def crop_all() -> None:
    try:
        from PIL import Image, ImageOps
    except ImportError:
        raise SystemExit("readme photos: Pillow is missing, run `uv sync` to install the dev group") from None

    CARD_IMAGES.mkdir(parents=True, exist_ok=True)
    for name, (src, w, h, fx, fy) in JOBS.items():
        im = ImageOps.exif_transpose(Image.open(ROOT / src)).convert("RGB")
        box = crop_box(*im.size, w, h, fx, fy)
        im = im.crop(box).resize((round(w * SCALE), round(h * SCALE)), Image.LANCZOS)
        path = CARD_IMAGES / f"{name}.jpg"
        im.save(path, quality=74, optimize=True, progressive=True)
        print(f"{name:20} crop={box} -> {path.stat().st_size // 1024} KB")
