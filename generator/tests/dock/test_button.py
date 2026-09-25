from xml.etree import ElementTree

import pytest

from readme.dock.button import DockButton
from readme.dock.enum import DockEnumIcon
from readme.dock.link import DockLink
from readme.svg.theme import SvgTheme


@pytest.mark.parametrize("icon", tuple(DockEnumIcon))
def test_every_icon_renders_a_well_formed_button(
    icon: DockEnumIcon, theme: SvgTheme
) -> None:
    button = DockButton(
        link=DockLink(
            label="Label & co", href="https://example.com", icon=icon
        ),
        width=250,
        radius=16,
        first=True,
        last=True,
        bottom=True,
    )

    svg = button.render(theme).render()

    ElementTree.fromstring(svg)
    assert "Label &amp; co" in svg


def test_only_bottom_corners_are_rounded() -> None:
    link = DockLink(label="x", href="#", icon=DockEnumIcon.DOC)

    assert (
        DockButton(
            link=link,
            width=100,
            radius=16,
            first=True,
            last=True,
            bottom=False,
        ).radius_left
        == 0
    )
    assert (
        DockButton(
            link=link,
            width=100,
            radius=16,
            first=True,
            last=False,
            bottom=True,
        ).radius_left
        == 16
    )
    assert (
        DockButton(
            link=link,
            width=100,
            radius=16,
            first=True,
            last=False,
            bottom=True,
        ).radius_right
        == 0
    )
