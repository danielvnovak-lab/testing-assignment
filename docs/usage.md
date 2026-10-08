# Usage

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. All commands below assume you are in the project root.

## Running `main.py`

> uv run main.py

## Building the library

> uv build

## Installing dependencies from `pyproject.toml`

> uv sync

## Running tests

> uv run pytest

## Running tests with coverage

> uv run pytest --cov=src/ --cov-report=html:htmlcov
