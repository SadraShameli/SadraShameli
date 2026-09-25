from dataclasses import dataclass
from typing import ClassVar

from readme import constants
from readme.card.enum import CardEnumName
from readme.card.project.info import CardProjectInfo, CardProjectInfoSpec
from readme.card.project.photo_base import CardProjectPhotoBase
from readme.dock.dock import Dock
from readme.dock.enum import DockEnumIcon
from readme.dock.link import DockLink
from readme.photo.enum import PhotoEnumName


@dataclass(kw_only=True, slots=True)
class CardProjectSensorhub(CardProjectPhotoBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.PROJECT_SENSORHUB
    ALT: ClassVar[str] = (
        "SensorHub: ESP32 sensor units I design, 3D-print and program. They report climate and "
        "loudness to sadra.nl."
    )
    DOCK: ClassVar[Dock | None] = Dock(
        href=constants.URL_REPOSITORY_SENSORHUB,
        rows=(
            (
                DockLink(
                    label="Source code",
                    href=constants.URL_REPOSITORY_SENSORHUB,
                    icon=DockEnumIcon.GITHUB,
                ),
                DockLink(
                    label="Spin the enclosure in 3D",
                    href=constants.URL_SENSORHUB_ENCLOSURE,
                    icon=DockEnumIcon.CUBE,
                ),
            ),
        ),
    )
    INFO: ClassVar[CardProjectInfo] = CardProjectInfo(
        title="SensorHub",
        eyebrow="IOT · FIRMWARE · HARDWARE",
        period="2024 — NOW",
        description="Sensor units I design in Fusion 360, 3D-print and program. They measure climate "
        "and loudness, record audio when it gets loud, and report to sadra.nl over HTTPS.",
        specs=(
            CardProjectInfoSpec(
                key="firmware",
                value="C++ · ESP-IDF 6 · FreeRTOS service kernel",
            ),
            CardProjectInfoSpec(
                key="sensors",
                value="BME680 climate · INMP441 mic · SSD1306 OLED",
            ),
            CardProjectInfoSpec(
                key="audio", value="own IMA-ADPCM encoder · 5 s pre-roll"
            ),
            CardProjectInfoSpec(
                key="ci",
                value="30 host-side unit tests · clang-tidy · cppcheck",
            ),
        ),
    )
    PHOTO: ClassVar[PhotoEnumName] = PhotoEnumName.SENSORHUB
    CHIP: ClassVar[str] = "ESP32 · FREERTOS · 3D PRINTED"
    CHIP_COLOR: ClassVar[str] = "#22c55e"
