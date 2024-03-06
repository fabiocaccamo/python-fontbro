#!/bin/bash

mypy fontbro --install-types --non-interactive
coverage erase
coverage run --append --show-missing unittest discover
coverage report -m
