from xml.sax.saxutils import escape


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def pct(time: float, total: float) -> str:
    return (
        f"{min(max(time / total * 100, 0), 100):.3f}".rstrip("0").rstrip(".")
        + "%"
    )
