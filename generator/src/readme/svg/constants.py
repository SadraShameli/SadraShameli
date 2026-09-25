from pathlib import Path

SVG_NAMESPACE = "http://www.w3.org/2000/svg"
SVG_COLOR_BLACK = "#000"
SVG_COLOR_WHITE = "#fff"
SVG_MONO_ADVANCE = 0.6
SVG_CLIP_ID = "clip"
SVG_CLIP_GROUP = f'<g clip-path="url(#{SVG_CLIP_ID})">'
SVG_REDUCED_MOTION_CSS = (
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
)
SVG_JPEG_DATA_PREFIX = "data:image/jpeg;base64,"
SVG_SHOWCASE_RATIO = 1.6

SVG_FONT_DIRECTORY = Path(__file__).resolve().parent / "fonts"
SVG_FONT_METRICS = SVG_FONT_DIRECTORY / "metrics.json"
SVG_FONT_SUFFIX = ".woff2"
SVG_FONT_FALLBACK_GLYPH = "n"
