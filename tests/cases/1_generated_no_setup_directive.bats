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
    bind 'set enable-bracketed-paste off'
}

# Teardown function
function run_teardown () {
    : # Nothing here...
}

@test "test of line 4" {
    run_setup "test-of-line-4"

    # Assertion of line 4
	shopt -s expand_aliases
	print_debug "$(echo "Hi Mom!")" "$(echo -e 'Hi Mom!\n')"
	[ "$(echo "Hi Mom!")" == "$(echo -e 'Hi Mom!\n')" ]

    run_teardown
}

@test "test of line 7" {
    run_setup "test-of-line-7"

    # Assertion of line 7
	shopt -s expand_aliases
	print_debug "$(echo 'Hello world' | wc -l)" "$(echo -e '1\n')"
	[ "$(echo 'Hello world' | wc -l)" == "$(echo -e '1\n')" ]

    run_teardown
}
