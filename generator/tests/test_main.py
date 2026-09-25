from pathlib import Path
from unittest.mock import patch

import pytest

from readme import constants
from readme.main import main


def test_help_lists_the_commands(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.argv", ["readme", "--help"])

    main()

    output = capsys.readouterr().out
    assert "build" in output
    assert "photos" in output


def test_outside_the_repository_exits_with_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["readme", "build"])

    with (
        patch.object(constants, "PATH_PACKAGE", tmp_path),
        pytest.raises(SystemExit) as exit_info,
    ):
        main()

    assert exit_info.value.code == constants.EXIT_CODE_FAILURE
    assert "No profile repository" in capsys.readouterr().err
