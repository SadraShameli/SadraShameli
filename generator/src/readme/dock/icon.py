from dataclasses import dataclass
from typing import ClassVar

from readme.dock.constants import (
    DOCK_ICON_PATH_GITHUB,
    DOCK_ICON_PATH_LINKEDIN,
    DOCK_ICON_PATH_YOUTUBE,
)
from readme.dock.enum import DockEnumIcon


@dataclass(kw_only=True, frozen=True, slots=True)
class DockIcon:
    SIZE: ClassVar[int] = 16

    icon: DockEnumIcon
    x: float
    center_y: float
    color: str

    @property
    def translate(self) -> str:
        return f"translate({self.x:.1f} {self.center_y - self.SIZE / 2:.1f})"

    def render(self) -> str:
        match self.icon:
            case DockEnumIcon.GITHUB:
                return self._brand(DOCK_ICON_PATH_GITHUB)
            case DockEnumIcon.YOUTUBE:
                return self._brand(DOCK_ICON_PATH_YOUTUBE)
            case DockEnumIcon.LINKEDIN:
                return self._brand(DOCK_ICON_PATH_LINKEDIN)
            case DockEnumIcon.PLAY:
                return f'<path transform="{self.translate}" d="M4 2l10 6-10 6z" fill="{self.color}"/>'
            case DockEnumIcon.GLOBE:
                return self._outline(
                    '<circle cx="8" cy="8" r="7"/><ellipse cx="8" cy="8" rx="3" ry="7"/><path d="M1 8h14"/>'
                )
            case DockEnumIcon.MAIL:
                return self._outline(
                    '<rect x="1" y="3" width="14" height="10" rx="2"/><path d="M1.5 4l6.5 5 6.5-5"/>'
                )
            case DockEnumIcon.DOC:
                return self._outline(
                    '<path d="M3 1h7l3 3v11H3z"/><path d="M10 1v3h3M5.5 8h5M5.5 11h5"/>'
                )
            case DockEnumIcon.CUBE:
                return self._outline(
                    '<path d="M8 1l6.5 3.5v7L8 15l-6.5-3.5v-7z"/><path d="M1.5 4.5L8 8l6.5-3.5M8 8v7"/>'
                )

    def _brand(self, path: str) -> str:
        return f'<path transform="{self.translate} scale(.6667)" d="{path}" fill="{self.color}"/>'

    def _outline(self, shapes: str) -> str:
        return (
            f'<g transform="{self.translate}" fill="none" stroke="{self.color}" stroke-width="1.5" '
            f'stroke-linecap="round" stroke-linejoin="round">{shapes}</g>'
        )
