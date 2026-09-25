from xml.etree import ElementTree

from readme.svg.constants import SVG_NAMESPACE
from readme.svg.document import SvgDocument


def test_render_is_well_formed_and_escapes_text() -> None:
    svg = SvgDocument(
        width=100,
        height=50.5,
        body="<rect/>",
        css="rect{fill:red}",
        title="a & b",
        description='say "hi"',
    ).render()
    root = ElementTree.fromstring(svg)

    assert root.get("width") == "100"
    assert root.get("height") == "50.5"
    assert root.findtext(f"{{{SVG_NAMESPACE}}}title") == "a & b"
    assert root.findtext(f"{{{SVG_NAMESPACE}}}desc") == 'say "hi"'


def test_render_leaves_out_an_empty_description() -> None:
    svg = SvgDocument(width=1, height=1, body="", css="", title="t").render()

    assert "<desc>" not in svg
