#!/bin/bash

mypy fontbro --follow-imports="skip" --ignore-missing-imports --install-types --non-interactive --strict
coverage erase
coverage run --append --source=fontbro -m unittest
coverage report -m --show-missing --ignore-errors
