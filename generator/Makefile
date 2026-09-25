.DEFAULT_GOAL := build

PACKAGE_NAME = readme

.PHONY: install
install:
	uv sync

.PHONY: update
update:
	uv lock --upgrade
	uv sync

.PHONY: build
build:
	uv run $(PACKAGE_NAME) build

.PHONY: photos
photos:
	uv run $(PACKAGE_NAME) photos

.PHONY: tests
tests:
	uv run pytest

.PHONY: format
format:
	-uv run pre-commit run --all-files --hook-stage manual
	-uv run ruff check --fix
	uv run ruff format

.PHONY: lint
lint: format
	uv run pre-commit run --all-files --hook-stage pre-push

.PHONY: clean
clean:
	git clean -Xdf
