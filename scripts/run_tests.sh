#!/usr/bin/env bash


echo -n "unit tests:"
export PYTHONPATH=${PYTHONPATH}:src
pytest src
