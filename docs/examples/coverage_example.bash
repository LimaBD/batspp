#!/bin/bash
#
# This is how coverage reports can
# be generated for Bats files
#
# We need to exclude Bats related files
#

this_folder=$(dirname $(realpath -s $0))
cd $this_folder
kcov --exclude-pattern=/usr/lib/,/tmp/bats-run $this_folder/report/ bats ./generated_bash_example.bats 
