import pytest

from readme.svg.constants import SVG_FONT_DIRECTORY, SVG_FONT_SUFFIX
from readme.svg.enum import (
    SvgEnumFont,
    SvgEnumFontFamily,
    SvgEnumFontWeight,
)


def test_font_family_and_weight_come_from_the_member_name() -> None:
    assert SvgEnumFont.MONO_SEMIBOLD.family is SvgEnumFontFamily.MONO
    assert SvgEnumFont.MONO_SEMIBOLD.weight is SvgEnumFontWeight.SEMIBOLD
    assert SvgEnumFont.DISPLAY_EXTRABOLD.weight == 800


@pytest.mark.parametrize("font", tuple(SvgEnumFont))
def test_every_font_ships_a_file(font: SvgEnumFont) -> None:
    assert (SVG_FONT_DIRECTORY / f"{font}{SVG_FONT_SUFFIX}").is_file()


@pytest.mark.parametrize("family", tuple(SvgEnumFontFamily))
def test_every_family_stack_starts_with_its_own_face(
    family: SvgEnumFontFamily,
) -> None:
    assert family.stack.startswith(f"'{family}',")
