"""Build the README graphics.

    python Scripts/readme static            # -> Assets/Readme
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from svg import ROOT, THEMES

STATIC_OUT = ROOT / "Assets" / "Readme"


def build_static(out: Path) -> None:
    from about import about
    from cards import all_cards
    from footer import footer
    from hero import hero
    from stack import stack
    from terminal import documents, paths, youtube

    out.mkdir(parents=True, exist_ok=True)
    for t in THEMES:
        files = {
            "hero": hero(t),
            "about": about(t),
            "stack": stack(t),
            "youtube": youtube(t),
            "documents": documents(t),
            "footer": footer(t),
            **paths(t),
            **all_cards(t),
        }
        for name, svg in files.items():
            (out / f"{name}-{t.name}.svg").write_text(svg, encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="readme")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("static")
    parser.parse_args(argv)
    build_static(STATIC_OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
