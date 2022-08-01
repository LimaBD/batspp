#!/usr/bin/env bats
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp
#

# Constants
VERBOSE_DEBUG="| hexdump -C"
TEMP_DIR="/tmp/batspp-27320"

# One time global setup
shopt -s expand_aliases
source /home/angrygingy/Desktop/work-repos/batspp/docs/examples/bash_example.bash

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
	print_debug "$(test-of-line-15-line15-actual)" "$(test-of-line-15-line15-expected)"
	[ "$(test-of-line-15-line15-actual)" == "$(test-of-line-15-line15-expected)" ]

	run_teardown
}

function test-of-line-15-line15-actual () {
	echo -e "hello\nworld"
}

function test-of-line-15-line15-expected () {
	echo -e 'hello\nworld'
}

@test "test of line 24" {
	run_setup "test-of-line-24"

	# Assertion of line 24
	print_debug "$(test-of-line-24-line24-actual)" "$(test-of-line-24-line24-expected)"
	[ "$(test-of-line-24-line24-actual)" == "$(test-of-line-24-line24-expected)" ]

	run_teardown
}

function test-of-line-24-line24-actual () {
	fibonacci 9
}

function test-of-line-24-line24-expected () {
	echo -e '0 1 1 2 3 5 8 13 21 34'
}

@test "test of line 27" {
	run_setup "test-of-line-27"

	# Assertion of line 27
	print_debug "$(test-of-line-27-line27-actual)" "$(test-of-line-27-line27-expected)"
	[ "$(test-of-line-27-line27-actual)" != "$(test-of-line-27-line27-expected)" ]

	run_teardown
}

function test-of-line-27-line27-actual () {
	fibonacci 3
}

function test-of-line-27-line27-expected () {
	echo -e '8 2 45 34 3 5'
}

@test "test of line 59" {
	run_setup "test-of-line-59"

	# Assertion of line 59
	print_debug "$(test-of-line-59-line59-actual)" "$(test-of-line-59-line59-expected)"
	[ "$(test-of-line-59-line59-actual)" == "$(test-of-line-59-line59-expected)" ]

	run_teardown
}

function test-of-line-59-line59-actual () {
	run-fibonacci 9
}

function test-of-line-59-line59-expected () {
	echo -e 'The Fibonacci series is:\n0 1 1 2 3 5 8 13 21 34'
}

@test "test of line 71" {
	run_setup "test-of-line-71"

	# Assertion of line 73
	filepath=$(echo $TMP/testfile-"$$")
	echo "this is a file content to run an example test" | sudo tee $filepath
	print_debug "$(test-of-line-71-line73-actual)" "$(test-of-line-71-line73-expected)"
	[ "$(test-of-line-71-line73-actual)" == "$(test-of-line-71-line73-expected)" ]

	run_teardown
}

function test-of-line-71-line73-actual () {
	cat $filepath
}

function test-of-line-71-line73-expected () {
	echo -e 'this is a file content to run an example test'
}

@test "test of line 79" {
	run_setup "test-of-line-79"

	# Assertion of line 81
	filepath=$(echo $TMP/testfile-"$$")
	echo -e "in this test\nwe are using\nmultiple assertions" | sudo tee $filepath
	print_debug "$(test-of-line-79-line81-actual)" "$(test-of-line-79-line81-expected)"
	[ "$(test-of-line-79-line81-actual)" == "$(test-of-line-79-line81-expected)" ]

	# Assertion of line 83
	print_debug "$(test-of-line-79-line83-actual)" "$(test-of-line-79-line83-expected)"
	[ "$(test-of-line-79-line83-actual)" == "$(test-of-line-79-line83-expected)" ]

	run_teardown
}

function test-of-line-79-line81-actual () {
	cat $filepath | wc -l
}

function test-of-line-79-line81-expected () {
	echo -e '3'
}

function test-of-line-79-line83-actual () {
	cat $filepath | wc -c
}

function test-of-line-79-line83-expected () {
	echo -e '46'
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
