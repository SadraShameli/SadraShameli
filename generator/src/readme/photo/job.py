from dataclasses import dataclass
from pathlib import Path

from readme.photo.constants import PHOTO_SCALE
from readme.photo.enum import PhotoEnumName
from readme.photo.frame import PhotoFrame


@dataclass(kw_only=True, frozen=True, slots=True)
class PhotoJob:
    name: PhotoEnumName
    source: Path
    frame: PhotoFrame
    focus_x: float
    focus_y: float

    @property
    def size(self) -> tuple[int, int]:
        return (
            round(self.frame.width * PHOTO_SCALE),
            round(self.frame.height * PHOTO_SCALE),
        )

    def crop_box(self, width: int, height: int) -> tuple[int, int, int, int]:
        aspect = self.frame.ratio

        if width / height > aspect:
            crop_width, crop_height = round(height * aspect), height
        else:
            crop_width, crop_height = width, round(width / aspect)

        left = min(
            max(round(self.focus_x * width - crop_width / 2), 0),
            width - crop_width,
        )
        top = min(
            max(round(self.focus_y * height - crop_height / 2), 0),
            height - crop_height,
        )

        return left, top, left + crop_width, top + crop_height
