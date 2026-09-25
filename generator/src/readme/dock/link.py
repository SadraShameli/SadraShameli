from dataclasses import dataclass

from readme.dock.enum import DockEnumIcon


@dataclass(kw_only=True, frozen=True, slots=True)
class DockLink:
    label: str
    href: str
    icon: DockEnumIcon
