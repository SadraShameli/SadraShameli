"""Build the README graphics.

    python Scripts/readme static            # -> Assets/Readme, and repoints README.md

Every file name carries a hash of its contents (hero-dark.1a2b3c4d.svg). A
changed card gets a new URL, so browsers and GitHub's cache can never show an
old card next to its new link buttons.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

from svg import ROOT, THEMES

STATIC_OUT = ROOT / "Assets" / "Readme"


def build_static(out: Path) -> None:
    from about import about
    from cards import all_cards
    from dock import all_docks
    from footer import footer
    from hero import hero
    from intro import intro
    from terminal import documents, paths, youtube

    (out / "dock").mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}  # "hero-dark" -> Assets/Readme/hero-dark.<hash>.svg
    for t in THEMES:
        files = {
            "hero": hero(t),
            "intro": intro(t),
            "about": about(t),
            "youtube": youtube(t),
            "documents": documents(t),
            "footer": footer(t),
            **paths(t),
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


def _repoint_readme(out: Path, written: dict[str, Path]) -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    prefix = out.relative_to(ROOT).as_posix()
    for stem, path in written.items():
        pattern = rf"{re.escape(prefix)}/{re.escape(stem)}(?:\.[0-9a-f]{{8}})?\.svg"
        text = re.sub(pattern, path.relative_to(ROOT).as_posix(), text)
    readme.write_text(text, encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="readme")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("static")
    parser.parse_args(argv)
    build_static(STATIC_OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
