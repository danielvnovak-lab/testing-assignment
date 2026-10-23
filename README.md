# 31282 Systems Testing and Quality Management Assignment 3

## Overview

This repository contains the work for Testing Assignment 3.

## Testing website

The assignment originally used the LambdaTest E-Commerce Playground, which the
instructor has taken offline. Per the course announcement, testing now uses:

[OpenCart demo](https://opencart.abstracta.us/index.php?route=common/home)

It runs the same OpenCart software and demo catalogue (same routes, field IDs
and messages) as the old playground, so the existing scenarios carry over.
The `BASE_URL` environment variable still overrides the target.

## Running the tests

From the repository root:

```bash
uv sync              # first time only: install dependencies
uv run pytest -v     # run all tests (headed: browser window is visible)
HEADLESS=1 uv run pytest -v     # run all tests (headless)
```

> Note: this is a shared public demo. OpenCart can answer repeated failed
> logins with 'account has exceeded allowed number of login attempts'; the
> suite already accepts that as a valid rejection.

## Assignment instructions

- [Git basics](docs/git-basics.md)
- [Docker setup](.devcontainer/README.md)
- [Usage](docs/usage.md)
