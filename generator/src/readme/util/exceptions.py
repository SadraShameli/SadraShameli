from pathlib import Path

from readme.exceptions import ReadmeError


class UtilExceptionRepositoryNotFoundError(ReadmeError, FileNotFoundError):
    def __init__(self, *, starts: tuple[Path, ...]) -> None:
        super().__init__(
            "No profile repository (a README.md next to Assets/Readme) at "
            f"or above {', '.join(f"'{start}'" for start in starts)}"
        )
