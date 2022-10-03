#!/bin/bash
#
# This is how coverage reports can
# be generated for Bats files
#
# We need to exclude Bats related files
#

kcov --exclude-pattern=/usr/lib/,/tmp/bats-run ./report/ bats ./generated_bash_example.bats 
