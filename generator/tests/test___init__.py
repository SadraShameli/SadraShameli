import ast
import io
import tokenize
from pathlib import Path

import pytest

from readme import constants
from tests.conftest import PATH_TESTS, modules, parse

PACKAGE_MODULES = modules(constants.PATH_PACKAGE)
SOURCE_MODULES = PACKAGE_MODULES + modules(PATH_TESTS)
ROOT_PREFIX = "Readme"


def camel(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def class_prefix(module: Path) -> str:
    *folders, stem = (
        module.relative_to(constants.PATH_PACKAGE).with_suffix("").parts
    )
    prefix = "".join(camel(folder) for folder in folders) or ROOT_PREFIX

    if stem == "exceptions":
        return prefix if not folders else f"{prefix}Exception"

    if stem == "enum":
        return f"{prefix}Enum"

    if not folders or stem in folders:
        return prefix

    if stem.startswith(f"{folders[-1]}_"):
        return prefix + camel(stem.removeprefix(f"{folders[-1]}_"))

    return prefix + camel(stem)


@pytest.mark.parametrize("module", SOURCE_MODULES, ids=str)
def test_module_has_no_comments(module: Path) -> None:
    tokens = tokenize.generate_tokens(
        io.StringIO(module.read_text(encoding="utf-8")).readline
    )
    comments = [
        f"{module}:{token.start[0]}"
        for token in tokens
        if token.type == tokenize.COMMENT
    ]

    assert comments == []


@pytest.mark.parametrize("module", SOURCE_MODULES, ids=str)
def test_module_has_no_docstrings(module: Path) -> None:
    documented = [
        getattr(node, "name", module.name)
        for node in ast.walk(parse(module))
        if isinstance(
            node,
            ast.Module | ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
        )
        and ast.get_docstring(node, clean=False) is not None
    ]

    assert documented == []


@pytest.mark.parametrize("module", PACKAGE_MODULES, ids=str)
def test_class_names_mirror_the_folder_path(module: Path) -> None:
    prefix = class_prefix(module)
    misnamed = [
        node.name
        for node in parse(module).body
        if isinstance(node, ast.ClassDef) and not node.name.startswith(prefix)
    ]

    assert misnamed == [], f"classes in {module} must start with {prefix}"


@pytest.mark.parametrize("module", PACKAGE_MODULES, ids=str)
def test_dataclasses_are_keyword_only_with_slots(module: Path) -> None:
    loose = [
        node.name
        for node in parse(module).body
        if isinstance(node, ast.ClassDef)
        for decorator in node.decorator_list
        if (isinstance(decorator, ast.Name) and decorator.id == "dataclass")
        or (
            isinstance(decorator, ast.Call)
            and isinstance(decorator.func, ast.Name)
            and decorator.func.id == "dataclass"
            and not {"kw_only", "slots"}
            <= {
                keyword.arg
                for keyword in decorator.keywords
                if isinstance(keyword.value, ast.Constant)
                and keyword.value.value is True
            }
        )
    ]

    assert loose == []


def test_every_test_folder_is_a_package() -> None:
    folders = {module.parent for module in modules(PATH_TESTS)}

    assert [
        folder for folder in folders if not (folder / "__init__.py").is_file()
    ] == []
