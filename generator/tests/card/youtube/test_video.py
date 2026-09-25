import pytest

from readme.card.youtube.video import CardYoutubeVideo
from readme.photo.enum import PhotoEnumName


@pytest.mark.parametrize(
    ("views", "label"),
    [
        (42, "42 views"),
        (513, "500+ views"),
        (999, "900+ views"),
        (1000, "1k+ views"),
        (1197, "1.1k+ views"),
        (2720, "2.7k+ views"),
    ],
)
def test_views_label_rounds_down(views: int, label: str) -> None:
    video = CardYoutubeVideo(
        file="video.mp4",
        title="Video",
        views=views,
        date="Dec 2022",
        thumbnail=PhotoEnumName.YT_INDOOR_TEST,
    )

    assert video.views_label == label
