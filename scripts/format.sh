#!/bin/sh -e

set -x

ruff check bot scripts --fix
ruff format bot scripts