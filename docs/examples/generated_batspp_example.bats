#!/usr/bin/env bats
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp

# Setup
shopt -s expand_aliases
source ./bash_example.bash


@test "test of line 17" {
	test_folder=$(echo /tmp/test-of-line-17-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 17
	actual=$(test-of-line-17-line17-actual)
	expected=$(test-of-line-17-line17-expected)
	print_debug "$actual" "$expected"
	[ "$actual" == "$expected" ]
}

function test-of-line-17-line17-actual () {
	echo -e "hello\nworld"
}

function test-of-line-17-line17-expected () {
	echo -e 'hello\nworld'
}

@test "test of line 23" {
	test_folder=$(echo /tmp/test-of-line-23-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 23
	actual=$(test-of-line-23-line23-actual)
	expected=$(test-of-line-23-line23-expected)
	print_debug "$actual" "$expected"
	[ "$actual" == "$expected" ]
}

function test-of-line-23-line23-actual () {
	run-fibonacci 9
}

function test-of-line-23-line23-expected () {
	echo -e 'The Fibonacci series is:\n0 1 1 2 3 5 8 13 21 34'
}

@test "setup and title" {
	test_folder=$(echo /tmp/setup-and-title-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 34
	filepath=$(echo $TMP/testfile-"$$")
	echo -n "this is a file content to run an example test" | sudo tee $filepath
	actual=$(setup-and-title-line34-actual)
	expected=$(setup-and-title-line34-expected)
	print_debug "$actual" "$expected"
	[ "$actual" == "$expected" ]

	# Assertion of line 45
	echo -n " using setup" >> $filepath
	echo -n " and continue directives" >> $filepath
	actual=$(setup-and-title-line45-actual)
	expected=$(setup-and-title-line45-expected)
	print_debug "$actual" "$expected"
	[ "$actual" == "$expected" ]
}

function setup-and-title-line34-actual () {
	cat $filepath
}

function setup-and-title-line34-expected () {
	echo -e 'this is a file content to run an example test'
}

function setup-and-title-line45-actual () {
	cat $filepath
}

function setup-and-title-line45-expected () {
	echo -e 'this is a file content to run an example test using setup and continue directives'
}

@test "test of line 50" {
	test_folder=$(echo /tmp/test-of-line-50-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 52
	filepath=$(echo $TMP/testfile-"$$")
	echo -e "in this test\nwe are using\nmultiple assertions" | sudo tee $filepath
	actual=$(test-of-line-50-line52-actual)
	expected=$(test-of-line-50-line52-expected)
	print_debug "$actual" "$expected"
	[ "$actual" == "$expected" ]

	# Assertion of line 54
	actual=$(test-of-line-50-line54-actual)
	expected=$(test-of-line-50-line54-expected)
	print_debug "$actual" "$expected"
	[ "$actual" == "$expected" ]
}

function test-of-line-50-line52-actual () {
	cat $filepath | wc -l
}

function test-of-line-50-line52-expected () {
	echo -e '3'
}

function test-of-line-50-line54-actual () {
	cat $filepath | wc -c
}

function test-of-line-50-line54-expected () {
	echo -e '46'
}

# This prints debug data when an assertion fail
# $1 -> actual
# $2 -> expected
function print_debug() {
	echo "========== actual =========="
	echo "$1"
	echo "========= expected ========="
	echo "$2"
	echo "============================"
}
