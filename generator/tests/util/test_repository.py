from pathlib import Path
from unittest.mock import patch

import pytest

from readme import constants
from readme.photo.enum import PhotoEnumName
from readme.util.exceptions import UtilExceptionRepositoryNotFoundError
from readme.util.repository import UtilRepository


def test_locate_walks_up_to_the_profile_repository(
    repository: UtilRepository, monkeypatch: pytest.MonkeyPatch
) -> None:
    nested = repository.root / "some" / "folder"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)

    with patch.object(constants, "PATH_PACKAGE", nested):
        assert UtilRepository.locate() == repository


def test_locate_fails_loud_outside_a_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    with (
        patch.object(constants, "PATH_PACKAGE", tmp_path),
        pytest.raises(UtilExceptionRepositoryNotFoundError),
    ):
        UtilRepository.locate()


def test_paths_are_rooted_in_the_repository(
    repository: UtilRepository,
) -> None:
    assert repository.readme == repository.root / "README.md"
    assert repository.photo(PhotoEnumName.SENSORHUB).name == "sensorhub.jpg"
    assert repository.relative(repository.assets) == "Assets/Readme"
