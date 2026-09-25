import ast
from pathlib import Path

import pytest

from readme import constants
from tests.conftest import modules, parse

BOOTSTRAP = (
    constants.PATH_PACKAGE / "__init__.py",
    constants.PATH_PACKAGE / "main.py",
)
LOGGER_PACKAGE = constants.PATH_PACKAGE / "logger"
FEATURE_MODULES = [
    module
    for module in modules(constants.PATH_PACKAGE)
    if module not in BOOTSTRAP and LOGGER_PACKAGE not in module.parents
]


def is_logger_call(node: ast.expr) -> bool:
    return isinstance(node, ast.Call) and (
        (isinstance(node.func, ast.Name) and node.func.id == "get_logger")
        or (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "getLogger"
        )
    )


@pytest.mark.parametrize("module", FEATURE_MODULES, ids=str)
def test_loggers_are_created_once_at_module_level(module: Path) -> None:
    tree = parse(module)
    module_loggers = [
        node.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and [
            target.id
            for target in node.targets
            if isinstance(target, ast.Name)
        ]
        == ["logger"]
        and is_logger_call(node.value)
    ]
    inline = [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and is_logger_call(node)
        and node not in module_loggers
    ]

    assert len(module_loggers) <= 1
    assert inline == []
