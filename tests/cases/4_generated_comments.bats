#!/usr/bin bats
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp
#

# Constants
VERBOSE_DEBUG="| hexdump -C"
TEMP_DIR="/tmp/batspp-'<REPLACED>'"

# One time global setup
source '<REPLACED>'

# Setup function
# $1 -> test name
function run_setup () {
    test_folder=$(echo $TEMP_DIR/$1-$$)
    mkdir --parents "$test_folder"
    cd "$test_folder" || echo Warning: Unable to "cd $test_folder"
}

# Teardown function
function run_teardown () {
    : # Nothing here...
}

@test "test of line 1" {
    run_setup "test-of-line-1"

    # Assertion of line 1
	shopt -s expand_aliases
	print_debug "$(echo "Hello World!")" "$(echo -e 'Hello World!\n')"
	[ "$(echo "Hello World!")" == "$(echo -e 'Hello World!\n')" ]

    run_teardown
}
