"""Where things live: the repository this package draws the README for, and its own data files."""

from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
FONTS = PACKAGE / "fonts"
ICONS = PACKAGE / "icons.json"
NOT_IN_REPO = "readme: run this from inside the profile repository"


def _repo_root() -> Path:
    # The package lives in <repo>/generator/src/readme and uv installs it in editable
    # mode. The working directory is tried first so a regular install works from inside
    # the repo too.
    for start in (Path.cwd(), PACKAGE):
        for folder in (start, *start.parents):
            if (folder / "Assets" / "Readme").is_dir() and (
                folder / "README.md"
            ).is_file():
                return folder
    raise SystemExit(NOT_IN_REPO)


ROOT = _repo_root()
README = ROOT / "README.md"
ASSETS = ROOT / "Assets" / "Readme"  # generated cards
CARD_IMAGES = ROOT / "Images" / "Cards"  # photos cropped for the cards
DOCUMENTS_DIR = ROOT / "Documents"
