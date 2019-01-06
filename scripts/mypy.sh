#!/usr/bin/env bash

export MYPYPATH=${PWD}/src
echo "Defined mypy path: ${MYPYPATH}"
mypy -p src --ignore-missing-imports --config-file mypy.ini