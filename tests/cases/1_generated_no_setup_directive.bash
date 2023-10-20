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

function test-of-line-4 {
    run_setup "test-of-line-4"

    # Assertion of line 4
    shopt -s expand_aliases
    if [ "$(echo "Hi Mom!")" == "$(echo -e 'Hi Mom!\n')" ]
    then
        : # keep
    else
        print_debug "$(echo "Hi Mom!")" "$(echo -e 'Hi Mom!\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "test of line 4" "test-of-line-4"

function test-of-line-7 {
    run_setup "test-of-line-7"

    # Assertion of line 7
    shopt -s expand_aliases
    if [ "$(echo 'Hello world' | wc -l)" == "$(echo -e '1\n')" ]
    then
        : # keep
    else
        print_debug "$(echo 'Hello world' | wc -l)" "$(echo -e '1\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "test of line 7" "test-of-line-7"

# Summary function
function print_summary {
    echo ""
    echo "Short summary: $bad failed, $good passed."
}
print_summary
