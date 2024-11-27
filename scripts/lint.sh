#!/usr/bin/env bash

set -e
set -x

mypy bot
ruff check bot
ruff format bot --check