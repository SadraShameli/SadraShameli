import pytest

from readme.svg.enum import SvgEnumTheme
from readme.svg.theme import SvgTheme


@pytest.mark.parametrize("name", tuple(SvgEnumTheme))
def test_of_builds_the_named_theme(name: SvgEnumTheme) -> None:
    assert SvgTheme.of(name).name is name


def test_themes_differ() -> None:
    assert SvgTheme.of(SvgEnumTheme.DARK) != SvgTheme.of(SvgEnumTheme.LIGHT)
