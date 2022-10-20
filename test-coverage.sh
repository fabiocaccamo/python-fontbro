#!/bin/bash

coverage erase
coverage run -m unittest
coverage report -m
