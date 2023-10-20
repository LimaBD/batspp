#!/usr/bin bash
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp
#

# Function to run tests and keep track of results
# $1 => name
# $2 => test function
n=0
good=0
bad=0
function run_test {
    local name="$1"
    local test="$2"
    let n++
    result=""
    $test
    if [ $? -eq 0 ]
    then
        let good++
        result=ok
    else
        let bad++
        result="not ok"
    fi
    echo "$result $n $name"
}

# This prints debug data when an assertion fail
# $1 -> actual value
# $2 -> expected value
function print_debug() {
    echo ""
    echo "=======  actual  ======="
    bash -c "echo \"$1\" $VERBOSE_DEBUG"
    echo "======= expected ======="
    bash -c "echo \"$2\" $VERBOSE_DEBUG"
    echo "========================"
}

# Constants
VERBOSE_DEBUG="| hexdump -C"
TEMP_DIR="/tmp/batspp-<REPLACED>"

# One time global setup
shopt -s expand_aliases
source <REPLACED>

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

function test-of-line-15 {
    run_setup "test-of-line-15"

    # Assertion of line 15
    shopt -s expand_aliases
    if [ "$(echo -e "hello\nworld")" == "$(echo -e 'hello\nworld\n')" ]
    then
        : # keep
    else
        print_debug "$(echo -e "hello\nworld")" "$(echo -e 'hello\nworld\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "test of line 15" "test-of-line-15"

function test-of-line-20 {
    run_setup "test-of-line-20"

    # Assertion of line 20
    shopt -s expand_aliases
    if [ "$(run-fibonacci 9)" == "$(echo -e 'The Fibonacci series is:\n0 1 1 2 3 5 8 13 21 34\n')" ]
    then
        : # keep
    else
        print_debug "$(run-fibonacci 9)" "$(echo -e 'The Fibonacci series is:\n0 1 1 2 3 5 8 13 21 34\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "test of line 20" "test-of-line-20"

function test-of-line-27 {
    run_setup "test-of-line-27"

    # Assertion of line 27
    shopt -s expand_aliases
    if [ "$(fibonacci 9)" == "$(echo -e '0 1 1 2 3 5 8 13 21 34\n')" ]
    then
        : # keep
    else
        print_debug "$(fibonacci 9)" "$(echo -e '0 1 1 2 3 5 8 13 21 34\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "test of line 27" "test-of-line-27"

function test-of-line-30 {
    run_setup "test-of-line-30"

    # Assertion of line 30
    shopt -s expand_aliases
    if [ "$(fibonacci 3)" != "$(echo -e '8 2 45 34 3 5\n')" ]
    then
        : # keep
    else
        print_debug "$(fibonacci 3)" "$(echo -e '8 2 45 34 3 5\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "test of line 30" "test-of-line-30"

function setup-and-title {
    run_setup "setup-and-title"

    # Assertion of line 38
    filepath=$(echo $TMP/testfile-"$$")
    echo -n "this is a file content to run an example test" | sudo tee $filepath
    shopt -s expand_aliases
    if [ "$(cat $filepath)" == "$(echo -e 'this is a file content to run an example test\n')" ]
    then
        : # keep
    else
        print_debug "$(cat $filepath)" "$(echo -e 'this is a file content to run an example test\n')"
        return 1
    fi

    # Assertion of line 48
    echo -n " using setup" >> $filepath
    echo -n " and continue directives" >> $filepath
    shopt -s expand_aliases
    if [ "$(cat $filepath)" == "$(echo -e 'this is a file content to run an example test using setup and continue directives\n')" ]
    then
        : # keep
    else
        print_debug "$(cat $filepath)" "$(echo -e 'this is a file content to run an example test using setup and continue directives\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "setup and title" "setup-and-title"

function test-of-line-52 {
    run_setup "test-of-line-52"

    # Assertion of line 54
    filepath=$TMP/testfile-"$$"
    echo -e "in this test\nwe are using\nmultiple assertions" > $filepath
    shopt -s expand_aliases
    if [ "$(cat $filepath | wc -l)" == "$(echo -e '3\n')" ]
    then
        : # keep
    else
        print_debug "$(cat $filepath | wc -l)" "$(echo -e '3\n')"
        return 1
    fi

    # Assertion of line 56
    shopt -s expand_aliases
    if [ "$(cat $filepath | wc -c)" == "$(echo -e '46\n')" ]
    then
        : # keep
    else
        print_debug "$(cat $filepath | wc -c)" "$(echo -e '46\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "test of line 52" "test-of-line-52"

# Summary function
function print_summary {
    echo ""
    echo "Short summary: $bad failed, $good passed."
}
print_summary
