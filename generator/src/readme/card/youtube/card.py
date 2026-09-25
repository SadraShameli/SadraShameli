from dataclasses import dataclass
from typing import ClassVar

from readme import constants
from readme.card.card_base import CardBase
from readme.card.constants import CARD_TERMINAL_RADIUS
from readme.card.enum import CardEnumName
from readme.card.terminal import CardTerminal
from readme.card.youtube.video import CardYoutubeVideo
from readme.dock.dock import Dock
from readme.dock.enum import DockEnumIcon
from readme.dock.link import DockLink
from readme.photo.constants import PHOTO_FRAME_THUMBNAIL
from readme.photo.enum import PhotoEnumName
from readme.svg.box import SvgBox
from readme.svg.constants import SVG_COLOR_BLACK, SVG_COLOR_WHITE
from readme.svg.document import SvgDocument
from readme.svg.enum import SvgEnumFont, SvgEnumFontFamily
from readme.svg.font import SvgFont
from readme.svg.photo import SvgPhoto
from readme.svg.util import esc


@dataclass(kw_only=True, slots=True)
class CardYoutube(CardBase):
    NAME: ClassVar[CardEnumName] = CardEnumName.YOUTUBE
    ALT: ClassVar[str] = (
        "Terminal listing my top YouTube videos: line detection for A.I. (2.7k+ views), range "
        "detection with lidar (1.1k+ views) and my self-driving robot's first indoor test (500+ views)"
    )
    DOCK: ClassVar[Dock | None] = Dock(
        href=constants.URL_YOUTUBE,
        rows=(
            (
                DockLink(
                    label="Line detection",
                    href=constants.URL_VIDEO_LINE_DETECTION,
                    icon=DockEnumIcon.PLAY,
                ),
                DockLink(
                    label="Lidar ranging",
                    href=constants.URL_VIDEO_LIDAR_RANGING,
                    icon=DockEnumIcon.PLAY,
                ),
                DockLink(
                    label="Indoor test drive",
                    href=constants.URL_VIDEO_INDOOR_TEST,
                    icon=DockEnumIcon.PLAY,
                ),
                DockLink(
                    label="Channel",
                    href=constants.URL_YOUTUBE,
                    icon=DockEnumIcon.YOUTUBE,
                ),
            ),
        ),
    )
    SPACED: ClassVar[bool] = True
    RADIUS: ClassVar[int] = CARD_TERMINAL_RADIUS
    MARGIN: ClassVar[int] = 36
    CWD: ClassVar[str] = "~/youtube"
    VIDEOS: ClassVar[tuple[CardYoutubeVideo, ...]] = (
        CardYoutubeVideo(
            file="line-detection.mp4",
            title="Line detection for A.I. based on contrast difference",
            views=2720,
            date="Dec 2022",
            thumbnail=PhotoEnumName.YT_LINE_DETECTION,
        ),
        CardYoutubeVideo(
            file="lidar-ranging.mp4",
            title="Range detection for A.I. based on lidar",
            views=1197,
            date="Dec 2022",
            thumbnail=PhotoEnumName.YT_LIDAR_RANGING,
        ),
        CardYoutubeVideo(
            file="indoor-test.mp4",
            title="Testing my self-driving robot indoors",
            views=513,
            date="Dec 2022",
            thumbnail=PhotoEnumName.YT_INDOOR_TEST,
        ),
    )

    def render(self) -> SvgDocument:
        term = CardTerminal(
            theme=self.theme, title=f"sadra@rijswijk: {self.CWD}"
        )
        x0, cmd_y = self.MARGIN, 84
        done = term.command(x0, cmd_y, self.CWD, "ls --sort=views | head -3")
        top = cmd_y + 30
        col_w = (self.WIDTH - 2 * x0) / len(self.VIDEOS)

        for i, video in enumerate(self.VIDEOS):
            term.body.append(
                self._video(
                    term.appear(done + 0.25 + i * 0.18, 0.35),
                    i,
                    video,
                    SvgBox(
                        x=x0 + i * col_w,
                        y=top,
                        width=col_w,
                        height=PHOTO_FRAME_THUMBNAIL.height,
                    ),
                )
            )

        prompt_y = top + PHOTO_FRAME_THUMBNAIL.height + 44
        end = done + 0.25 + len(self.VIDEOS) * 0.18 + 0.3
        term.cursor(term.prompt(x0, prompt_y, self.CWD), prompt_y, end)

        return term.render(
            frame=self.frame(prompt_y + 30),
            fonts=(
                SvgEnumFont.MONO_REGULAR,
                SvgEnumFont.MONO_SEMIBOLD,
                SvgEnumFont.SANS_REGULAR,
            ),
            description="; ".join(
                f"{video.title} ({video.views_label})" for video in self.VIDEOS
            ),
        )

    def _video(
        self, appearance: str, index: int, video: CardYoutubeVideo, box: SvgBox
    ) -> str:
        t = self.theme
        x, top = box.x, box.y
        thumb_w, thumb_h = (
            PHOTO_FRAME_THUMBNAIL.width,
            PHOTO_FRAME_THUMBNAIL.height,
        )
        tx = x + thumb_w + 18
        text_w = box.width - thumb_w - 18 - 16
        pcx, pcy = x + thumb_w / 2, top + thumb_h / 2
        clip = f"th{index}"
        photo = SvgPhoto(
            path=self.context.repository.photo(video.thumbnail),
            box=SvgBox(x=x, y=top, width=thumb_w, height=thumb_h),
            clip=clip,
        )
        lines = "".join(
            f'<text x="{tx:.1f}" y="{top + 44 + i * 20}" font-family="{SvgEnumFontFamily.SANS.stack}" '
            f'font-size="14" fill="{t.muted}">{esc(line)}</text>'
            for i, line in enumerate(
                SvgFont.wrap(video.title, SvgEnumFont.SANS_REGULAR, 14, text_w)
            )
        )

        return (
            f'<g class="{appearance}">'
            f'<clipPath id="{clip}"><rect x="{x}" y="{top}" width="{thumb_w}" height="{thumb_h}" rx="10"/>'
            "</clipPath>"
            + photo.render(t)
            + f'<rect x="{x + 0.5}" y="{top + 0.5}" width="{thumb_w - 1}" height="{thumb_h - 1}" rx="10" '
            f'fill="none" stroke="{t.border}"/>'
            f'<circle cx="{pcx}" cy="{pcy}" r="19" fill="{SVG_COLOR_BLACK}" fill-opacity=".6" '
            f'stroke="{SVG_COLOR_WHITE}" stroke-opacity=".5"/>'
            f'<path d="M{pcx - 5} {pcy - 8}L{pcx + 8} {pcy}L{pcx - 5} {pcy + 8}Z" fill="{SVG_COLOR_WHITE}"/>'
            f'<text x="{tx:.1f}" y="{top + 16}" fill="{t.text}" font-weight="600">{esc(video.file)}</text>'
            + lines
            + f'<text x="{tx:.1f}" y="{top + thumb_h - 26}" font-size="12" fill="{t.green}">'
            f"{esc(video.views_label)}</text>"
            f'<text x="{tx:.1f}" y="{top + thumb_h - 6}" font-size="12" fill="{t.faint}">{esc(video.date)}</text>'
            "</g>"
        )
