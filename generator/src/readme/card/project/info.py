from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True, slots=True)
class CardProjectInfoSpec:
    key: str
    value: str


@dataclass(kw_only=True, frozen=True, slots=True)
class CardProjectInfo:
    title: str
    eyebrow: str
    period: str
    description: str
    specs: tuple[CardProjectInfoSpec, ...] = ()
