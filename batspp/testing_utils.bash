#!/usr/bin bash
#
# Batspp testing utils
#

# This prints debug data when an assertion fail
# $1 -> actual value
# $2 -> expected value
function print_debug() {
    echo ""
    echo "=======  actual  ======="
    bash -c "echo \\\"$1\\\" ${VERBOSE_DEBUG}"
    echo "======= expected ======="
    bash -c "echo \\\"$2\\\" ${VERBOSE_DEBUG}"
    echo "========================"
}

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

# Summary function
function print_summary {
    echo ""
    echo "Short summary: $bad failed, $good passed."
}
