#!/usr/bin/env bats
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp
#

# Constants
VERBOSE_DEBUG="| hexdump -C"
TEMP_DIR="/tmp/batspp-83095"

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
	print_debug "$(test-of-line-4-line4-actual)" "$(test-of-line-4-line4-expected)"
	[ "$(test-of-line-4-line4-actual)" == "$(test-of-line-4-line4-expected)" ]

	run_teardown
}

function test-of-line-4-line4-actual () {
	echo "Hi Mom!"
}

function test-of-line-4-line4-expected () {
	echo -e 'Hi Mom!'
}

@test "test of line 7" {
	run_setup "test-of-line-7"

	# Assertion of line 7
	print_debug "$(test-of-line-7-line7-actual)" "$(test-of-line-7-line7-expected)"
	[ "$(test-of-line-7-line7-actual)" == "$(test-of-line-7-line7-expected)" ]

	run_teardown
}

function test-of-line-7-line7-actual () {
	echo 'Hello world' | wc -l
}

function test-of-line-7-line7-expected () {
	echo -e '1'
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
