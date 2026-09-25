"""Where things live: the repository this package draws the README for, and its own data files."""

from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
FONTS = PACKAGE / "fonts"
ICONS = PACKAGE / "icons.json"


def _repo_root() -> Path:
    # uv installs the project in editable mode, so the package normally sits in <repo>/src/readme.
    # The working directory is tried first so a regular install still works from inside the repo.
    for start in (Path.cwd(), PACKAGE):
        for folder in (start, *start.parents):
            if (folder / "pyproject.toml").is_file() and (folder / "Assets").is_dir():
                return folder
    raise SystemExit("readme: run this from inside the profile repository")


ROOT = _repo_root()
README = ROOT / "README.md"
ASSETS = ROOT / "Assets" / "Readme"  # generated cards
CARD_IMAGES = ROOT / "Images" / "Cards"  # photos cropped for the cards
DOCUMENTS_DIR = ROOT / "Documents"
