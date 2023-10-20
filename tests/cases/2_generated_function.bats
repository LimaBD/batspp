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

    # Assertion of line 17
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
	shopt -s expand_aliases
	print_debug "$(fibonacci 9)" "$(echo -e '0 1 1 2 3 5 8 13 21 34\n')"
	[ "$(fibonacci 9)" == "$(echo -e '0 1 1 2 3 5 8 13 21 34\n')" ]

    run_teardown
}

@test "test of line 20" {
    run_setup "test-of-line-20"

    # Assertion of line 21
    function line-wc () { perl -n -e '@_ = split; printf("%d\t%s", 1 + $\#_, $_);' "$@"; }
	shopt -s expand_aliases
	print_debug "$(echo -e "hello\nworld!" | line-wc)" "$(echo -e '1       hello\n1       world!\n')"
	[ "$(echo -e "hello\nworld!" | line-wc)" == "$(echo -e '1       hello\n1       world!\n')" ]

    run_teardown
}

@test "test of line 26" {
    run_setup "test-of-line-26"

    # Assertion of line 29
    function hello () {
    echo "hello world!"
    }
	shopt -s expand_aliases
	print_debug "$(hello)" "$(echo -e 'hello world!\n')"
	[ "$(hello)" == "$(echo -e 'hello world!\n')" ]

    run_teardown
}
