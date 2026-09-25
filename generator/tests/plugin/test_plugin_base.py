from enum import StrEnum
from pathlib import Path
from typing import ClassVar

from readme.plugin.plugin_base import PluginBase
from readme.plugin.registry import PluginRegistry


class PluginBaseProbeEnum(StrEnum):
    ONLY = "only"


class PluginBaseProbeFile(StrEnum):
    PLUGIN = "plugin.py"


def test_only_classes_that_declare_a_name_register() -> None:
    probes: PluginRegistry[PluginBaseProbeEnum, PluginBase] = PluginRegistry(
        enum=PluginBaseProbeEnum,
        package=__name__,
        anchor=Path(__file__).parent,
        file=PluginBaseProbeFile.PLUGIN,
    )

    class PluginBaseProbe(PluginBase, registry=probes):
        NAME: ClassVar[PluginBaseProbeEnum]

    class PluginBaseProbeIntermediate(PluginBaseProbe):
        pass

    class PluginBaseProbeLeaf(PluginBaseProbeIntermediate):
        NAME = PluginBaseProbeEnum.ONLY

    assert probes.ordered() == (PluginBaseProbeLeaf,)
