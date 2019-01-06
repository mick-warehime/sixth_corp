#!/usr/bin/env bash

# style enforcement - (exclude views because pyqt output is verbose/unwieldy/
# not our code)
echo -n "flake8 style check: "
flake8 src
echo "done."

#  run unit tests and coverage
echo -n "unit tests:"
export PYTHONPATH=${PYTHONPATH}:src
pytest src
