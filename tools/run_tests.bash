#!/bin/bash
#
# Run tests and generate HTML coverage
#
# Usage examples:
#   $ run_tests.bash 
#   $ run_tests.bash -m "<PYTEST-MARKER-EXPRESSION>"
#
## TODO: save older runned htmlcovs.

base=$(dirname $(realpath -s $0))/..
tests=$base/tests

echo -e "Running tests on $tests\n"

export PYTHONPATH="$base/:$PYTHONPATH"
export COVERAGE_RCFILE="$base/.coveragerc"

coverage run -m pytest $tests "$@"
coverage combine
coverage html --directory $tests/htmlcov
