#!/bin/bash

mypy fontbro --install-types --non-interactive --strict
coverage erase
coverage run --append --show-missing unittest discover
coverage report -m
