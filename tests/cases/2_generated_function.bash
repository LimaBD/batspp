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
}

# Teardown function
function run_teardown () {
    : # Nothing here...
}

function test-of-line-1 {
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
run_test "test of line 1" "test-of-line-1"

function test-of-line-20 {
    run_setup "test-of-line-20"

    # Assertion of line 21
    function line-wc () { perl -n -e '@_ = split; printf("%d\t%s", 1 + $\#_, $_);' "$@"; }
    shopt -s expand_aliases
    if [ "$(echo -e "hello\nworld!" | line-wc)" == "$(echo -e '1       hello\n1       world!\n')" ]
    then
        : # keep
    else
        print_debug "$(echo -e "hello\nworld!" | line-wc)" "$(echo -e '1       hello\n1       world!\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "test of line 20" "test-of-line-20"

function test-of-line-26 {
    run_setup "test-of-line-26"

    # Assertion of line 29
    function hello () {
    echo "hello world!"
    }
    shopt -s expand_aliases
    if [ "$(hello)" == "$(echo -e 'hello world!\n')" ]
    then
        : # keep
    else
        print_debug "$(hello)" "$(echo -e 'hello world!\n')"
        return 1
    fi

    run_teardown
    return 0
}
run_test "test of line 26" "test-of-line-26"

# Summary function
function print_summary {
    echo ""
    echo "Short summary: $bad failed, $good passed."
}
print_summary
