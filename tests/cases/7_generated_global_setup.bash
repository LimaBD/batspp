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
    alias count-words='wc -w'
}

# Teardown function
function run_teardown () {
    : # Nothing here...
}

function word-count-1 {
    run_setup "word-count-1"

    # Assertion of line 7
    shopt -s expand_aliases
    if [ "$(echo abc | count-words)" == "$(echo -e '1\n')" ]
    then
        : # keep
    else
        print_debug "$(echo abc | count-words)" "$(echo -e '1\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "word count 1" "word-count-1"

function word-count-2 {
    run_setup "word-count-2"

    # Assertion of line 11
    shopt -s expand_aliases
    if [ "$(echo abc def ghi | count-words)" == "$(echo -e '3\n')" ]
    then
        : # keep
    else
        print_debug "$(echo abc def ghi | count-words)" "$(echo -e '3\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "word count 2" "word-count-2"

# Summary function
function print_summary {
    echo ""
    echo "Short summary: $bad failed, $good passed."
}
print_summary
