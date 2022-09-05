#!/bin/bash
#
# Run tests and generate coverage
#
## TODO: save older runned htmlcovs.

base=$(dirname $(realpath -s $0))/..
tests=$base/tests

echo -e "Running tests on $tests\n"
export PYTHONPATH="$base/:$PYTHONPATH"
coverage run -m pytest $tests
coverage html --directory $tests/htmlcov --omit="*/tests/test_*","*/__init__.py"
