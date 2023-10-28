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

    # Assertion of line 2
    alias hello='echo "Hello user!"'
	shopt -s expand_aliases
	print_debug "$(hello)" "$(echo -e 'Hello user!\n')"
	[ "$(hello)" == "$(echo -e 'Hello user!\n')" ]

    run_teardown
}

@test "test of line 7" {
    run_setup "test-of-line-7"

    # Assertion of line 9
    alias count-words='wc -w'
	shopt -s expand_aliases
	print_debug "$(echo abc def ght | count-words)" "$(echo -e '3\n')"
	[ "$(echo abc def ght | count-words)" == "$(echo -e '3\n')" ]

    run_teardown
}
