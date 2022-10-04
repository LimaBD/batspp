#!/usr/bin/env bats
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp
#

# Constants
VERBOSE_DEBUG=""
TEMP_DIR="/tmp/batspp-78899"

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

	# Assertion of line 14
	function fibonacci () {
	result=""
	a=0
	b=1
	for (( i=0; i<=$1; i++ ))
	do
	result="$result$a "
	fn=$((a + b))
	a=$b
	b=$fn
	done
	echo $result
	}
	print_debug "$(fibonacci 9)" "$(echo -e '0 1 1 2 3 5 8 13 21 34')"
	[ "$(fibonacci 9)" == "$(echo -e '0 1 1 2 3 5 8 13 21 34')" ]

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
