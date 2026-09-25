from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from PIL import Image, ImageOps

from readme.constants import BYTES_PER_KIB
from readme.logger.logger_base import LoggerBase
from readme.photo.constants import (
    PHOTO_FRAME_FEATURED,
    PHOTO_FRAME_SHOT,
    PHOTO_FRAME_THUMBNAIL,
    PHOTO_QUALITY,
)
from readme.photo.enum import PhotoEnumName
from readme.photo.job import PhotoJob
from readme.util.repository import UtilRepository


@dataclass(kw_only=True, slots=True)
class PhotoCropper(LoggerBase):
    JOBS: ClassVar[tuple[PhotoJob, ...]] = (
        PhotoJob(
            name=PhotoEnumName.SENSORHUB,
            source=Path("Images/SensorHub1.jpg"),
            frame=PHOTO_FRAME_FEATURED,
            focus_x=0.5,
            focus_y=0.58,
        ),
        PhotoJob(
            name=PhotoEnumName.PROJECTAI,
            source=Path("Images/ProjectAI.jpg"),
            frame=PHOTO_FRAME_FEATURED,
            focus_x=0.52,
            focus_y=0.55,
        ),
        PhotoJob(
            name=PhotoEnumName.SHOT_SADRA_NL,
            source=Path("Images/Screenshots/sadra-nl.jpg"),
            frame=PHOTO_FRAME_SHOT,
            focus_x=0.5,
            focus_y=0.0,
        ),
        PhotoJob(
            name=PhotoEnumName.SHOT_PROP_CALCULATOR,
            source=Path("Images/Screenshots/prop-calculator.jpg"),
            frame=PHOTO_FRAME_SHOT,
            focus_x=0.5,
            focus_y=0.0,
        ),
        PhotoJob(
            name=PhotoEnumName.SHOT_MINOMARKT_NL,
            source=Path("Images/Screenshots/minomarkt-nl.jpg"),
            frame=PHOTO_FRAME_SHOT,
            focus_x=0.5,
            focus_y=0.0,
        ),
        PhotoJob(
            name=PhotoEnumName.SHOT_ROBOT,
            source=Path("Images/Robot.jpg"),
            frame=PHOTO_FRAME_SHOT,
            focus_x=0.5,
            focus_y=0.5,
        ),
        PhotoJob(
            name=PhotoEnumName.YT_LINE_DETECTION,
            source=Path("Images/YouTube/1142rRZ3rzc.jpg"),
            frame=PHOTO_FRAME_THUMBNAIL,
            focus_x=0.5,
            focus_y=0.5,
        ),
        PhotoJob(
            name=PhotoEnumName.YT_LIDAR_RANGING,
            source=Path("Images/YouTube/_C8PnLK2SWA.jpg"),
            frame=PHOTO_FRAME_THUMBNAIL,
            focus_x=0.5,
            focus_y=0.5,
        ),
        PhotoJob(
            name=PhotoEnumName.YT_INDOOR_TEST,
            source=Path("Images/YouTube/abyVlfAETG0.jpg"),
            frame=PHOTO_FRAME_THUMBNAIL,
            focus_x=0.5,
            focus_y=0.5,
        ),
    )

    repository: UtilRepository

    def run(self) -> None:
        self.repository.photos.mkdir(parents=True, exist_ok=True)

        for job in self.JOBS:
            with Image.open(self.repository.root / job.source) as source:
                image = ImageOps.exif_transpose(source).convert("RGB")

            box = job.crop_box(*image.size)
            path = self.repository.photo(job.name)
            image.crop(box).resize(job.size, Image.Resampling.LANCZOS).save(
                path, quality=PHOTO_QUALITY, optimize=True, progressive=True
            )

            self.logger.info(
                "%-20s crop=%s -> %d KB",
                job.name,
                box,
                path.stat().st_size // BYTES_PER_KIB,
            )
