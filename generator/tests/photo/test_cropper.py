from readme.photo.cropper import PhotoCropper
from readme.photo.enum import PhotoEnumName
from readme.util.repository import UtilRepository


def test_every_photo_has_exactly_one_job() -> None:
    assert sorted(job.name for job in PhotoCropper.JOBS) == sorted(
        PhotoEnumName
    )


def test_every_source_photo_exists(
    real_repository: UtilRepository,
) -> None:
    assert [
        job.source
        for job in PhotoCropper.JOBS
        if not (real_repository.root / job.source).is_file()
    ] == []
