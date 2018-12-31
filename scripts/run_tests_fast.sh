#  run unit tests and coverage
echo -n "unit tests:"
export PYTHONPATH=${PYTHONPATH}:src
pytest src
