#!/bin/bash

coverage erase
coverage run -m unittest discover tests/
coverage report -m