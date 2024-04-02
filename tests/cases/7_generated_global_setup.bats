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
    alias count-words='wc -w'
}

# Teardown function
function run_teardown () {
    : # Nothing here...
}

@test "word count 1" {
    run_setup "word-count-1"

    # Assertion of line 7
	shopt -s expand_aliases
	print_debug "$(echo abc | count-words)" "$(echo -e '1\n')"
	[ "$(echo abc | count-words)" == "$(echo -e '1\n')" ]

    run_teardown
}

@test "word count 2" {
    run_setup "word-count-2"

    # Assertion of line 11
	shopt -s expand_aliases
	print_debug "$(echo abc def ghi | count-words)" "$(echo -e '3\n')"
	[ "$(echo abc def ghi | count-words)" == "$(echo -e '3\n')" ]

    run_teardown
}
