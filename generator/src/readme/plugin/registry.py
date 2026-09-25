from dataclasses import dataclass, field
from enum import StrEnum
from importlib import import_module
from pathlib import Path

from readme.plugin.exceptions import (
    PluginExceptionDuplicateError,
    PluginExceptionMemberNotRegisteredError,
)


@dataclass(kw_only=True, slots=True)
class PluginRegistry[K: StrEnum, B]:
    enum: type[K]
    package: str
    anchor: Path
    file: StrEnum
    _mapping: dict[K, type[B]] = field(default_factory=dict)

    def register(self, cls: type[B], key: K) -> None:
        if (existing := self._mapping.get(key)) is not None and (
            existing.__module__,
            existing.__qualname__,
        ) != (cls.__module__, cls.__qualname__):
            raise PluginExceptionDuplicateError(
                registry=self.enum.__name__,
                key=key,
                incoming=cls.__name__,
                existing=existing.__name__,
            )

        self._mapping[key] = cls

    def discover(self) -> None:
        for module in sorted(self.anchor.rglob(self.file)):
            parts = module.relative_to(self.anchor).with_suffix("").parts
            import_module(".".join((self.package, *parts)))

    def ordered(self) -> tuple[type[B], ...]:
        if missing := [
            str(member) for member in self.enum if member not in self._mapping
        ]:
            raise PluginExceptionMemberNotRegisteredError(
                registry=self.enum.__name__, members=missing
            )

        return tuple(self._mapping[member] for member in self.enum)
