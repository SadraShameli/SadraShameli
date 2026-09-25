from dataclasses import dataclass
from typing import ClassVar

from readme import constants
from readme.card.enum import CardEnumName
from readme.card.project.info import CardProjectInfo, CardProjectInfoSpec
from readme.card.project.photo_base import CardProjectPhotoBase
from readme.card.project.projectai.lidar import CardProjectProjectaiLidar
from readme.dock.dock import Dock
from readme.dock.enum import DockEnumIcon
from readme.dock.link import DockLink
from readme.photo.constants import PHOTO_FRAME_FEATURED
from readme.photo.enum import PhotoEnumName
from readme.svg.box import SvgBox
from readme.svg.fragment import SvgFragment


@dataclass(kw_only=True, slots=True)
class CardProjectProjectai(CardProjectPhotoBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.PROJECT_PROJECTAI
    ALT: ClassVar[str] = (
        "Project A.I.: a self-driving robot car with on-device TensorFlow inference, lidar and a "
        "3D-printed chassis"
    )
    DOCK: ClassVar[Dock | None] = Dock(
        href=constants.URL_REPOSITORY_PROJECTAI,
        rows=(
            (
                DockLink(
                    label="Source code",
                    href=constants.URL_REPOSITORY_PROJECTAI,
                    icon=DockEnumIcon.GITHUB,
                ),
                DockLink(
                    label="Watch it drive",
                    href=constants.URL_VIDEO_INDOOR_TEST,
                    icon=DockEnumIcon.PLAY,
                ),
            ),
        ),
    )
    INFO: ClassVar[CardProjectInfo] = CardProjectInfo(
        title="Project A.I.",
        eyebrow="ROBOTICS · COMPUTER VISION",
        period="2022",
        description="A self-driving robot car that follows a course and dodges obstacles with on-device "
        "TensorFlow inference. No cloud: lidar, a camera and a 3D-printed chassis.",
        specs=(
            CardProjectInfoSpec(
                key="vision", value="line detection · lidar range detection"
            ),
            CardProjectInfoSpec(
                key="firmware", value="multithreaded C++ control loop"
            ),
            CardProjectInfoSpec(
                key="override", value="PS4 / PS5 controller as a safety net"
            ),
            CardProjectInfoSpec(
                key="research",
                value="school thesis (PWS) on artificial intelligence",
            ),
        ),
    )
    PHOTO: ClassVar[PhotoEnumName] = PhotoEnumName.PROJECTAI
    CHIP: ClassVar[str] = "LIDAR SCAN"
    CHIP_COLOR: ClassVar[str] = CardProjectProjectaiLidar.GREEN
    LIDAR_AT: ClassVar[tuple[float, float]] = (0.476, 0.357)

    def overlay(self, shot: SvgBox) -> SvgFragment:
        photo = PHOTO_FRAME_FEATURED
        fx, fy = self.LIDAR_AT
        scale = max(shot.width / photo.width, shot.height / photo.height)
        dw, dh = photo.width * scale, photo.height * scale
        cx = (shot.width - dw) / 2 + fx * dw
        cy = (shot.height - dh) / 2 + fy * dh

        return CardProjectProjectaiLidar(
            cx=round(shot.x + cx), cy=round(shot.y + cy)
        ).render()
