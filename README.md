# 31282 Systems Testing and Quality Management Assignment 3

## Overview

This repository contains the work for Testing Assignment 3.

## Testing website

Use the following website for testing:

[LambdaTest E-Commerce Playground](https://ecommerce-playground.lambdatest.io/index.php?route=common/home)

## Running the tests

From the repository root:

```bash
uv sync              # first time only: install dependencies
uv run pytest -v     # run all tests (headed: browser window is visible)
HEADLESS=1 uv run pytest -v     # run all tests (headless)
```

> Note: the shop rate-limits failed logins (~10 per hour per IP). If tests
> start failing with 'account has exceeded allowed number of login attempts',
> wait up to an hour or run a single file instead.

## Assignment instructions

- [Git basics](docs/git-basics.md)
- [Docker setup](.devcontainer/README.md)
- [Usage](docs/usage.md)
