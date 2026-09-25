from pathlib import Path

from readme.photo.enum import PhotoEnumName
from readme.photo.frame import PhotoFrame
from readme.photo.job import PhotoJob


def job(focus_x: float, focus_y: float) -> PhotoJob:
    return PhotoJob(
        name=PhotoEnumName.SENSORHUB,
        source=Path("source.jpg"),
        frame=PhotoFrame(width=400, height=200),
        focus_x=focus_x,
        focus_y=focus_y,
    )


def test_crop_keeps_the_frame_ratio() -> None:
    left, top, right, bottom = job(0.5, 0.5).crop_box(1000, 1000)

    assert (right - left) / (bottom - top) == 2
    assert (left, right) == (0, 1000)


def test_crop_centres_on_the_focus_point() -> None:
    assert job(0.5, 0.5).crop_box(1000, 1000) == (0, 250, 1000, 750)


def test_crop_is_clamped_inside_the_source() -> None:
    assert job(0.5, 0.0).crop_box(1000, 1000)[1] == 0
    assert job(0.5, 1.0).crop_box(1000, 1000)[3] == 1000
    assert job(0.0, 0.5).crop_box(3000, 1000)[0] == 0
    assert job(1.0, 0.5).crop_box(3000, 1000)[2] == 3000


def test_size_is_scaled_up_for_sharp_screens() -> None:
    assert job(0.5, 0.5).size == (600, 300)
