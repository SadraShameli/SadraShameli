import inspect
from importlib import import_module
from pathlib import Path

import pytest

from readme import constants
from readme.exceptions import ReadmeError

EXCEPTION_MODULES = sorted(constants.PATH_PACKAGE.rglob("exceptions.py"))
FAMILY_SUFFIX = "ExceptionError"


def exceptions_of(module: Path) -> list[type[BaseException]]:
    name = ".".join(
        (
            constants.PATH_PACKAGE.name,
            *module.relative_to(constants.PATH_PACKAGE).with_suffix("").parts,
        )
    )

    return [
        member
        for _, member in inspect.getmembers(
            import_module(name), inspect.isclass
        )
        if issubclass(member, BaseException) and member.__module__ == name
    ]


@pytest.mark.parametrize("module", EXCEPTION_MODULES, ids=str)
def test_exceptions_subclass_readme_error(module: Path) -> None:
    assert all(
        issubclass(error, ReadmeError) and error.__name__.endswith("Error")
        for error in exceptions_of(module)
    )


@pytest.mark.parametrize("module", EXCEPTION_MODULES, ids=str)
def test_concrete_exceptions_carry_their_own_message(module: Path) -> None:
    silent = [
        error.__name__
        for error in exceptions_of(module)
        if error is not ReadmeError
        and not error.__name__.endswith(FAMILY_SUFFIX)
        and "__init__" not in vars(error)
    ]

    assert silent == []
