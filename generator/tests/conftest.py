import ast
from collections.abc import Iterator
from pathlib import Path

import pytest

from readme import constants
from readme.card.card_base import CARD_REGISTRY, CardBase
from readme.card.context import CardContext
from readme.logger.manager import get_logger
from readme.svg.enum import SvgEnumTheme
from readme.svg.theme import SvgTheme
from readme.util.repository import UtilRepository

PATH_TESTS = Path(__file__).resolve().parent


def modules(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*.py") if "__pycache__" not in path.parts
    )


def parse(module: Path) -> ast.Module:
    return ast.parse(module.read_text(encoding="utf-8"), filename=str(module))


@pytest.fixture(autouse=True)
def isolated_logger() -> Iterator[None]:
    logger = get_logger()
    handlers, level = list(logger.handlers), logger.level

    yield

    logger.handlers[:] = handlers
    logger.setLevel(level)


@pytest.fixture(scope="session")
def real_repository() -> UtilRepository:
    return UtilRepository.locate()


@pytest.fixture
def repository(
    tmp_path: Path, real_repository: UtilRepository
) -> UtilRepository:
    for path in (constants.PATH_PHOTOS, constants.PATH_DOCUMENTS):
        link = tmp_path / path
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(real_repository.root / path, target_is_directory=True)

    (tmp_path / constants.PATH_ASSETS).mkdir(parents=True)
    (tmp_path / constants.PATH_README).write_text("", encoding="utf-8")

    return UtilRepository(root=tmp_path)


@pytest.fixture(params=tuple(SvgEnumTheme))
def theme(request: pytest.FixtureRequest) -> SvgTheme:
    return SvgTheme.of(request.param)


@pytest.fixture
def context(theme: SvgTheme, real_repository: UtilRepository) -> CardContext:
    return CardContext(theme=theme, repository=real_repository)


@pytest.fixture(scope="session")
def cards() -> tuple[type[CardBase], ...]:
    CARD_REGISTRY.discover()

    return CARD_REGISTRY.ordered()
