#!/bin/bash

coverage erase
coverage run --source=fontbro setup.py test
coverage report -m
