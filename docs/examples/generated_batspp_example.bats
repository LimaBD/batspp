#!/usr/bin/env bats
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp


# Setup
shopt -s expand_aliases
source ./bash_example.bash


@test "test of line 13" {
	test_folder=$(echo /tmp/test-of-line-13-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 13
	actual=$(test-of-line-13-line13-actual)
	expected=$(test-of-line-13-line13-expected)
	echo "========== actual =========="
	echo "$actual"
	echo "========= expected ========="
	echo "$expected"
	echo "============================"
	[ "$actual" == "$expected" ]
}

function test-of-line-13-line13-actual () {
	echo -e "hello\nworld"
}

function test-of-line-13-line13-expected () {
	echo -e 'hello\nworld'
}

@test "test of line 19" {
	test_folder=$(echo /tmp/test-of-line-19-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 19
	actual=$(test-of-line-19-line19-actual)
	expected=$(test-of-line-19-line19-expected)
	echo "========== actual =========="
	echo "$actual"
	echo "========= expected ========="
	echo "$expected"
	echo "============================"
	[ "$actual" == "$expected" ]
}

function test-of-line-19-line19-actual () {
	run-fibonacci 9
}

function test-of-line-19-line19-expected () {
	echo -e 'The Fibonacci series is:\n0 1 1 2 3 5 8 13 21 34'
}

@test "setup and title" {
	test_folder=$(echo /tmp/setup-and-title-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 30
	filepath=$(echo $TMP/testfile-"$$")
	echo -n "this is a file content to run an example test" | sudo tee $filepath
	actual=$(setup-and-title-line30-actual)
	expected=$(setup-and-title-line30-expected)
	echo "========== actual =========="
	echo "$actual"
	echo "========= expected ========="
	echo "$expected"
	echo "============================"
	[ "$actual" == "$expected" ]

	# Assertion of line 41
	echo -n " using setup" >> $filepath
	echo -n " and continue directives" >> $filepath
	actual=$(setup-and-title-line41-actual)
	expected=$(setup-and-title-line41-expected)
	echo "========== actual =========="
	echo "$actual"
	echo "========= expected ========="
	echo "$expected"
	echo "============================"
	[ "$actual" == "$expected" ]
}

function setup-and-title-line30-actual () {
	cat $filepath
}

function setup-and-title-line30-expected () {
	echo -e 'this is a file content to run an example test'
}

function setup-and-title-line41-actual () {
	cat $filepath
}

function setup-and-title-line41-expected () {
	echo -e 'this is a file content to run an example test using setup and continue directives'
}

@test "test of line 46" {
	test_folder=$(echo /tmp/test-of-line-46-$$)
	mkdir $test_folder && cd $test_folder

	# Assertion of line 48
	filepath=$(echo $TMP/testfile-"$$")
	echo -e "in this test\nwe are using\nmultiple assertions" | sudo tee $filepath
	actual=$(test-of-line-46-line48-actual)
	expected=$(test-of-line-46-line48-expected)
	echo "========== actual =========="
	echo "$actual"
	echo "========= expected ========="
	echo "$expected"
	echo "============================"
	[ "$actual" == "$expected" ]

	# Assertion of line 50
	actual=$(test-of-line-46-line50-actual)
	expected=$(test-of-line-46-line50-expected)
	echo "========== actual =========="
	echo "$actual"
	echo "========= expected ========="
	echo "$expected"
	echo "============================"
	[ "$actual" == "$expected" ]
}

function test-of-line-46-line48-actual () {
	cat $filepath | wc -l
}

function test-of-line-46-line48-expected () {
	echo -e '3'
}

function test-of-line-46-line50-actual () {
	cat $filepath | wc -c
}

function test-of-line-46-line50-expected () {
	echo -e '46'
}
