from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class SvgFragment:
    body: str
    css: str = ""
