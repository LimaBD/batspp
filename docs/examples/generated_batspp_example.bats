#!/usr/bin/env bats
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp
#

# Setup
shopt -s expand_aliases
source ./bash_example.bash

@test "test of line 17" {
	test_folder=$(echo /tmp/test-of-line-17-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 17
	first=$(test-of-line-17-line17-first)
	second=$(test-of-line-17-line17-second)
	print_debug "$first" "$second"
	[ "$first" == "$second" ]
}

function test-of-line-17-line17-first () {
	echo -e "hello\nworld"
}

function test-of-line-17-line17-second () {
	echo -e 'hello\nworld'
}

@test "test of line 23" {
	test_folder=$(echo /tmp/test-of-line-23-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 23
	first=$(test-of-line-23-line23-first)
	second=$(test-of-line-23-line23-second)
	print_debug "$first" "$second"
	[ "$first" == "$second" ]
}

function test-of-line-23-line23-first () {
	run-fibonacci 9
}

function test-of-line-23-line23-second () {
	echo -e 'The Fibonacci series is:\n0 1 1 2 3 5 8 13 21 34'
}

@test "test of line 31" {
	test_folder=$(echo /tmp/test-of-line-31-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 31
	first=$(test-of-line-31-line31-first)
	second=$(test-of-line-31-line31-second)
	print_debug "$first" "$second"
	[ "$first" == "$second" ]
}

function test-of-line-31-line31-first () {
	fibonacci 9
}

function test-of-line-31-line31-second () {
	echo -e '0 1 1 2 3 5 8 13 21 34'
}

@test "test of line 34" {
	test_folder=$(echo /tmp/test-of-line-34-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 34
	first=$(test-of-line-34-line34-first)
	second=$(test-of-line-34-line34-second)
	print_debug "$first" "$second"
	[ "$first" != "$second" ]
}

function test-of-line-34-line34-first () {
	fibonacci 3
}

function test-of-line-34-line34-second () {
	echo -e '8 2 45 34 3 5'
}

@test "setup and title" {
	test_folder=$(echo /tmp/setup-and-title-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 43
	filepath=$(echo $TMP/testfile-"$$")
	echo -n "this is a file content to run an example test" | sudo tee $filepath
	first=$(setup-and-title-line43-first)
	second=$(setup-and-title-line43-second)
	print_debug "$first" "$second"
	[ "$first" == "$second" ]

	# Assertion of line 54
	echo -n " using setup" >> $filepath
	echo -n " and continue directives" >> $filepath
	first=$(setup-and-title-line54-first)
	second=$(setup-and-title-line54-second)
	print_debug "$first" "$second"
	[ "$first" == "$second" ]
}

function setup-and-title-line43-first () {
	cat $filepath
}

function setup-and-title-line43-second () {
	echo -e 'this is a file content to run an example test'
}

function setup-and-title-line54-first () {
	cat $filepath
}

function setup-and-title-line54-second () {
	echo -e 'this is a file content to run an example test using setup and continue directives'
}

@test "test of line 59" {
	test_folder=$(echo /tmp/test-of-line-59-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 61
	filepath=$(echo $TMP/testfile-"$$")
	echo -e "in this test\nwe are using\nmultiple assertions" | sudo tee $filepath
	first=$(test-of-line-59-line61-first)
	second=$(test-of-line-59-line61-second)
	print_debug "$first" "$second"
	[ "$first" == "$second" ]

	# Assertion of line 63
	first=$(test-of-line-59-line63-first)
	second=$(test-of-line-59-line63-second)
	print_debug "$first" "$second"
	[ "$first" == "$second" ]
}

function test-of-line-59-line61-first () {
	cat $filepath | wc -l
}

function test-of-line-59-line61-second () {
	echo -e '3'
}

function test-of-line-59-line63-first () {
	cat $filepath | wc -c
}

function test-of-line-59-line63-second () {
	echo -e '46'
}

# This prints debug data when an assertion fail
# $1 -> first value
# $2 -> second value
function print_debug() {
	echo "========== first value =========="
	echo "$1"
	echo "========== second value =========="
	echo "$2"
	echo "==========++++++=================="
}
