#!/bin/bash
#
# Run tests and generate coverage
#
## TODO: save older runned htmlcovs.

tests=$(dirname $(realpath -s $0))
echo -e "Running tests on $tests\n"
coverage run -m unittest discover $tests
coverage html --directory $tests/htmlcov
