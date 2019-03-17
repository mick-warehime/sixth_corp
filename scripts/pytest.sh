#!/usr/bin/env bash


echo -n "unit tests:"
export PYTHONPATH=${PYTHONPATH}:src
pytest --cov=src --cov-report term-missing:skip-covered src
