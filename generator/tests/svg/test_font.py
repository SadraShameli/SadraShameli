import pytest

from readme.svg.enum import SvgEnumFont
from readme.svg.font import SvgFont


@pytest.mark.parametrize("font", tuple(SvgEnumFont))
def test_measure_grows_with_text_and_spacing(font: SvgEnumFont) -> None:
    assert SvgFont.measure("", font, 14) == 0
    assert SvgFont.measure("ab", font, 14) > SvgFont.measure("a", font, 14)
    assert SvgFont.measure("abc", font, 14, 1) == pytest.approx(
        SvgFont.measure("abc", font, 14) + 2
    )


def test_measure_scales_with_size() -> None:
    small = SvgFont.measure("sadra", SvgEnumFont.SANS_REGULAR, 10)

    assert SvgFont.measure(
        "sadra", SvgEnumFont.SANS_REGULAR, 20
    ) == pytest.approx(small * 2)


def test_wrap_keeps_every_word_within_the_width() -> None:
    text = "the quick brown fox jumps over the lazy dog " * 3
    lines = SvgFont.wrap(text, SvgEnumFont.SANS_REGULAR, 14, 120)

    assert " ".join(lines) == " ".join(text.split())
    assert all(
        SvgFont.measure(line, SvgEnumFont.SANS_REGULAR, 14) <= 120
        for line in lines
    )


def test_css_embeds_each_face_once() -> None:
    css = SvgFont.css(SvgEnumFont.MONO_REGULAR, SvgEnumFont.SANS_SEMIBOLD)

    assert css.count("@font-face") == 2
    assert "font-family:'sgm';font-weight:400" in css
    assert "font-family:'sgs';font-weight:600" in css
