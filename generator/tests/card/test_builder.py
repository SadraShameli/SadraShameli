import re

from readme.card.builder import CardBuilder
from readme.card.card_base import CardBase
from readme.svg.enum import SvgEnumTheme
from readme.util.repository import UtilRepository

REFERENCE = re.compile(r'(?:src|srcset)="([^"]+\.svg)"')


def build(repository: UtilRepository) -> dict[str, bytes]:
    CardBuilder(repository=repository).run()

    return {
        repository.relative(path): path.read_bytes()
        for path in repository.assets.rglob("*.svg")
    } | {"README.md": repository.readme.read_bytes()}


def test_run_writes_every_card_and_dock_button_for_both_themes(
    repository: UtilRepository, cards: tuple[type[CardBase], ...]
) -> None:
    files = build(repository)
    links = sum(
        len(row) for card in cards if card.DOCK for row in card.DOCK.rows
    )

    assert len(files) - 1 == (len(cards) + links) * len(SvgEnumTheme)


def test_readme_references_exactly_the_written_cards(
    repository: UtilRepository,
) -> None:
    files = build(repository)
    references = set(
        REFERENCE.findall(files["README.md"].decode(encoding="utf-8"))
    )

    assert references == set(files) - {"README.md"}


def test_run_is_deterministic(repository: UtilRepository) -> None:
    assert build(repository) == build(repository)


def test_run_removes_stale_cards(repository: UtilRepository) -> None:
    stale = repository.assets / "dock" / "gone-0-0-dark.deadbeef.svg"
    stale.parent.mkdir(parents=True)
    stale.write_text("<svg/>", encoding="utf-8")

    build(repository)

    assert not stale.exists()
