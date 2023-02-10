#!/usr/bin/env bats
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp
#

# Constants
VERBOSE_DEBUG="| hexdump -C"
TEMP_DIR="/tmp/batspp-182722"

# One time global setup
shopt -s expand_aliases
source ./bash_example.bash

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

@test "test of line 15" {
	run_setup "test-of-line-15"

	# Assertion of line 15
	shopt -s expand_aliases
	print_debug "$(echo -e "hello\nworld")" "$(echo -e 'hello\nworld\n')"
	[ "$(echo -e "hello\nworld")" == "$(echo -e 'hello\nworld\n')" ]

	run_teardown
}

@test "test of line 20" {
	run_setup "test-of-line-20"

	# Assertion of line 20
	shopt -s expand_aliases
	print_debug "$(run-fibonacci 9)" "$(echo -e 'The Fibonacci series is:\n0 1 1 2 3 5 8 13 21 34\n')"
	[ "$(run-fibonacci 9)" == "$(echo -e 'The Fibonacci series is:\n0 1 1 2 3 5 8 13 21 34\n')" ]

	run_teardown
}

@test "test of line 27" {
	run_setup "test-of-line-27"

	# Assertion of line 27
	shopt -s expand_aliases
	print_debug "$(fibonacci 9)" "$(echo -e '0 1 1 2 3 5 8 13 21 34\n')"
	[ "$(fibonacci 9)" == "$(echo -e '0 1 1 2 3 5 8 13 21 34\n')" ]

	run_teardown
}

@test "test of line 30" {
	run_setup "test-of-line-30"

	# Assertion of line 30
	shopt -s expand_aliases
	print_debug "$(fibonacci 3)" "$(echo -e '8 2 45 34 3 5\n')"
	[ "$(fibonacci 3)" != "$(echo -e '8 2 45 34 3 5\n')" ]

	run_teardown
}

@test "setup and title" {
	run_setup "setup-and-title"

	# Assertion of line 38
	filepath=$(echo $TMP/testfile-"$$")
	echo -n "this is a file content to run an example test" | sudo tee $filepath
	shopt -s expand_aliases
	print_debug "$(cat $filepath)" "$(echo -e 'this is a file content to run an example test\n')"
	[ "$(cat $filepath)" == "$(echo -e 'this is a file content to run an example test\n')" ]

	# Assertion of line 48
	echo -n " using setup" >> $filepath
	echo -n " and continue directives" >> $filepath
	shopt -s expand_aliases
	print_debug "$(cat $filepath)" "$(echo -e 'this is a file content to run an example test using setup and continue directives\n')"
	[ "$(cat $filepath)" == "$(echo -e 'this is a file content to run an example test using setup and continue directives\n')" ]

	run_teardown
}

@test "test of line 52" {
	run_setup "test-of-line-52"

	# Assertion of line 54
	filepath=$(echo $TMP/testfile-"$$")
	echo -e "in this test\nwe are using\nmultiple assertions" | sudo tee $filepath
	shopt -s expand_aliases
	print_debug "$(cat $filepath | wc -l)" "$(echo -e '3\n')"
	[ "$(cat $filepath | wc -l)" == "$(echo -e '3\n')" ]

	# Assertion of line 56
	shopt -s expand_aliases
	print_debug "$(cat $filepath | wc -c)" "$(echo -e '46\n')"
	[ "$(cat $filepath | wc -c)" == "$(echo -e '46\n')" ]

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
