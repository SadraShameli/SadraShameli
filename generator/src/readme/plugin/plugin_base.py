from typing import Any, ClassVar

from readme.plugin.constants import PLUGIN_KEY_ATTRIBUTE
from readme.plugin.registry import PluginRegistry


class PluginBase:
    __slots__ = ()

    __plugin_registry__: ClassVar[PluginRegistry[Any, Any] | None] = None

    def __init_subclass__(
        cls,
        *,
        registry: PluginRegistry[Any, Any] | None = None,
        **kwargs: object,
    ) -> None:
        super().__init_subclass__(**kwargs)

        if registry is not None:
            cls.__plugin_registry__ = registry

            return

        if (reg := cls.__plugin_registry__) is None or (
            key := cls.__dict__.get(PLUGIN_KEY_ATTRIBUTE)
        ) is None:
            return

        reg.register(cls, key)
