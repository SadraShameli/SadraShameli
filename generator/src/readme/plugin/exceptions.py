from readme.exceptions import ReadmeError


class PluginExceptionError(ReadmeError, ValueError):
    pass


class PluginExceptionDuplicateError(PluginExceptionError):
    def __init__(
        self, *, registry: str, key: str, incoming: str, existing: str
    ) -> None:
        super().__init__(
            f"Duplicate plugin '{key}' in {registry} "
            f"({incoming} vs {existing})"
        )


class PluginExceptionMemberNotRegisteredError(PluginExceptionError):
    def __init__(self, *, registry: str, members: list[str]) -> None:
        super().__init__(
            f"No plugin registered in {registry} for: {', '.join(members)}"
        )
