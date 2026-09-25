from enum import StrEnum
from pathlib import Path

import pytest

from readme.plugin.exceptions import (
    PluginExceptionDuplicateError,
    PluginExceptionMemberNotRegisteredError,
)
from readme.plugin.registry import PluginRegistry


class PluginRegistryProbeEnum(StrEnum):
    FIRST = "first"
    SECOND = "second"


class PluginRegistryProbeFile(StrEnum):
    PLUGIN = "plugin.py"


def registry() -> PluginRegistry[PluginRegistryProbeEnum, object]:
    return PluginRegistry(
        enum=PluginRegistryProbeEnum,
        package=__name__,
        anchor=Path(__file__).parent,
        file=PluginRegistryProbeFile.PLUGIN,
    )


def test_ordered_follows_the_enum_not_registration_order() -> None:
    probes = registry()
    probes.register(int, PluginRegistryProbeEnum.SECOND)
    probes.register(str, PluginRegistryProbeEnum.FIRST)

    assert probes.ordered() == (str, int)


def test_ordered_fails_loud_on_a_missing_member() -> None:
    probes = registry()
    probes.register(str, PluginRegistryProbeEnum.FIRST)

    with pytest.raises(
        PluginExceptionMemberNotRegisteredError, match="second"
    ):
        probes.ordered()


def test_a_second_class_for_the_same_key_is_rejected() -> None:
    probes = registry()
    probes.register(str, PluginRegistryProbeEnum.FIRST)
    probes.register(str, PluginRegistryProbeEnum.FIRST)

    with pytest.raises(PluginExceptionDuplicateError):
        probes.register(int, PluginRegistryProbeEnum.FIRST)
