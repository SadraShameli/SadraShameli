"""One-off: crop/resize photos into the exact frames the cards use.

Needs Pillow (the card builder itself is stdlib-only and just embeds the
results):  pip install pillow && python Scripts/readme/prep_images.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "Images" / "Cards"
SCALE = 1.5  # retina-ish without bloating the SVGs

# name: (source, frame w, frame h, focus x, focus y)  focus = 0..1 in the source
JOBS = {
    "sensorhub": ("Images/SensorHub1.jpg", 400, 320, 0.5, 0.58),
    "projectai": ("Images/ProjectAI.jpg", 400, 320, 0.52, 0.55),
    "sadra-nl": ("Images/Screenshots/sadra-nl.jpg", 490, 250, 0.5, 0.28),
    "prop-calculator": ("Images/Screenshots/prop-calculator.jpg", 490, 250, 0.5, 0.0),
    "minomarkt-nl": ("Images/Screenshots/minomarkt-nl.jpg", 490, 250, 0.5, 0.25),
    "robot": ("Images/Robot.jpg", 245, 250, 0.5, 0.5),
    "socialrobot": ("Images/SocialRobot.jpg", 245, 250, 0.45, 0.5),
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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (src, w, h, fx, fy) in JOBS.items():
        im = ImageOps.exif_transpose(Image.open(ROOT / src)).convert("RGB")
        box = crop_box(*im.size, w, h, fx, fy)
        im = im.crop(box).resize((round(w * SCALE), round(h * SCALE)), Image.LANCZOS)
        path = OUT / f"{name}.jpg"
        im.save(path, quality=74, optimize=True, progressive=True)
        print(f"{name:16} crop={box} -> {path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
