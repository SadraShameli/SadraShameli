from dataclasses import dataclass
from pathlib import Path
from typing import Self

from readme import constants
from readme.photo.constants import PHOTO_SUFFIX
from readme.photo.enum import PhotoEnumName
from readme.util.exceptions import UtilExceptionRepositoryNotFoundError


@dataclass(kw_only=True, frozen=True, slots=True)
class UtilRepository:
    root: Path

    @classmethod
    def locate(cls) -> Self:
        starts = (Path.cwd(), constants.PATH_PACKAGE)

        for start in starts:
            for folder in (start, *start.parents):
                if (folder / constants.PATH_ASSETS).is_dir() and (
                    folder / constants.PATH_README
                ).is_file():
                    return cls(root=folder)

        raise UtilExceptionRepositoryNotFoundError(starts=starts)

    @property
    def readme(self) -> Path:
        return self.root / constants.PATH_README

    @property
    def assets(self) -> Path:
        return self.root / constants.PATH_ASSETS

    @property
    def photos(self) -> Path:
        return self.root / constants.PATH_PHOTOS

    @property
    def documents(self) -> Path:
        return self.root / constants.PATH_DOCUMENTS

    def photo(self, name: PhotoEnumName) -> Path:
        return self.photos / f"{name}{PHOTO_SUFFIX}"

    def relative(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()
