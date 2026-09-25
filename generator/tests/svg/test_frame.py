from readme.svg.constants import SVG_CLIP_GROUP
from readme.svg.frame import SvgFrame
from readme.svg.theme import SvgTheme


def test_closed_frame_is_a_rounded_rect(theme: SvgTheme) -> None:
    frame = SvgFrame(width=100, height=50, radius=16, open_bottom=False)

    assert frame.outline(theme).startswith("<rect")
    assert frame.open(theme).endswith(SVG_CLIP_GROUP)


def test_open_frame_leaves_the_bottom_edge_to_the_dock(
    theme: SvgTheme,
) -> None:
    frame = SvgFrame(width=100, height=50, radius=16, open_bottom=True)

    assert frame.outline(theme).startswith("<path")
    assert frame.clip_path().count("<rect") == 2
