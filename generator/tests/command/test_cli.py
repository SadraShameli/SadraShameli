from unittest.mock import patch

import pytest
from click.testing import CliRunner

from readme import constants
from readme.command.cli import cli
from readme.util.repository import UtilRepository


def test_without_a_command_it_builds(
    repository: UtilRepository, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(repository.root)

    with patch.object(constants, "PATH_PACKAGE", repository.root):
        result = CliRunner().invoke(cli, [])

    assert result.exit_code == 0
    assert repository.readme.read_text(encoding="utf-8")
    assert any(repository.assets.rglob("*.svg"))
