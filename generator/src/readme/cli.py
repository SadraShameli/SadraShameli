"""Command line: `uv run readme` draws every card and points README.md at them.

    uv run readme           # same as `readme build`
    uv run readme photos    # re-crop the photos first, after adding or changing one

Every file name carries a hash of its contents (hero-dark.1a2b3c4d.svg). A
changed card gets a new URL, so browsers and GitHub's cache can never show an
old card next to its new link buttons.
"""

import argparse
import hashlib
import re
from pathlib import Path

from .btop import btop
from .cards import all_cards
from .dock import all_docks
from .footer import footer
from .hero import hero
from .intro import intro
from .paths import ASSETS, README, ROOT
from .svg import THEMES
from .terminal import documents, youtube


def build(out: Path = ASSETS) -> None:
    (out / "dock").mkdir(parents=True, exist_ok=True)
    written: dict[
        str, Path
    ] = {}  # "hero-dark" -> Assets/Readme/hero-dark.<hash>.svg
    for t in THEMES:
        files = {
            "hero": hero(t),
            "intro": intro(t),
            "btop": btop(t),
            "youtube": youtube(t),
            "documents": documents(t),
            "footer": footer(t),
            **all_cards(t),
            **all_docks(t),
        }
        for name, svg in files.items():
            digest = hashlib.sha1(svg.encode()).hexdigest()[:8]
            path = out / f"{name}-{t.name}.{digest}.svg"
            path.write_text(svg, encoding="utf-8")
            written[f"{name}-{t.name}"] = path

    keep = set(written.values())
    for old in out.rglob("*.svg"):
        if old not in keep:
            old.unlink()
    _repoint_readme(out, written)
    print(
        f"readme: {len(written)} cards in {out.relative_to(ROOT).as_posix()}, README.md updated"
    )


def _repoint_readme(out: Path, written: dict[str, Path]) -> None:
    text = README.read_text(encoding="utf-8")
    prefix = out.relative_to(ROOT).as_posix()
    for stem, path in written.items():
        pattern = (
            rf"{re.escape(prefix)}/{re.escape(stem)}(?:\.[0-9a-f]{{8}})?\.svg"
        )
        text = re.sub(pattern, path.relative_to(ROOT).as_posix(), text)
    README.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="readme", description="Draw the cards for the profile README."
    )
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser(
        "build",
        help="draw every card into Assets/Readme and update README.md (the default)",
    )
    sub.add_parser(
        "photos",
        help="re-crop the photos the cards embed (needs Pillow from the dev group)",
    )
    args = parser.parse_args(argv)
    if args.cmd == "photos":
        from .photos import crop_all

        crop_all()
    else:
        build()
    return 0
