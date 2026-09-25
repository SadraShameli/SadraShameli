from readme.svg.util import esc, pct


def test_esc_escapes_markup_and_quotes() -> None:
    assert esc('a & "b" <c>') == "a &amp; &quot;b&quot; &lt;c&gt;"


def test_pct_clamps_and_trims() -> None:
    assert pct(-1, 10) == "0%"
    assert pct(5, 10) == "50%"
    assert pct(1, 3) == "33.333%"
    assert pct(20, 10) == "100%"
