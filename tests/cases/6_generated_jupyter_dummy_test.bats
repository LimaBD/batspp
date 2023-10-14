#!/usr/bin/env bats
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp
#

# Constants
VERBOSE_DEBUG="| hexdump -C"
TEMP_DIR="/tmp/batspp-<REPLACED>"

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

@test "test of line 2" {
	run_setup "test-of-line-2"

	# Assertion of line 2
	shopt -s expand_aliases
	print_debug "$(echo dummy)" "$(echo -e 'dummy\n')"
	[ "$(echo dummy)" == "$(echo -e 'dummy\n')" ]

	run_teardown
}

@test "test of line 6" {
	run_setup "test-of-line-6"

	# Assertion of line 6
	shopt -s expand_aliases
	print_debug "$(date | grep "oct 2020")" "$(echo -e '1\n')"
	[ "$(date | grep "oct 2020")" == "$(echo -e '1\n')" ]

	run_teardown
}

# This prints debug data when an assertion fail
# $1 -> actual value
# $2 -> expected value
function print_debug() {
	echo "=======  actual  ======="
	bash -c "echo \"$1\" $VERBOSE_DEBUG"
	echo "======= expected ======="
	bash -c "echo \"$2\" $VERBOSE_DEBUG"
	echo "========================"
}
