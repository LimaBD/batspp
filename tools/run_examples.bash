#!/bin/bash
#
# Run Batspp and save examples
# output and generated bats
#
# This must be runned when something
# is changed on the interpreter and 
# the output/generated files changes
#

tools=$(dirname $(realpath -s $0))
base=$tools/..
examples=$base/docs/examples
test_cases=$base/tests/cases

export PYTHONPATH="$base/:$PYTHONPATH"

# Run example saving output and generated file
# $1 -> folder path
# $2 -> test file
# $3 -> generated filename to save
# $4 -> output filename to save
function run_eg () {

    # Args
    folder=$1
    test_file=$2
    generated=$3
    output=$4

    # Set args to run
    script="python3 $base/batspp/batspp"
    test_file=$folder/$test_file
    generated=$folder/$generated
    output=$folder/$output

    # Print trace
    echo ">>>>>>>>>>>>>>>>>>> RUN"
    echo -e "script\t$script"
    echo -e "test test_file\t$test_file"
    echo -e "generated path\t$generated"
    echo -e "output path\t$output\n"

    # Run
    cd $folder
    $script --hexdump_debug --save $generated $test_file > $output
}

# Run example that starts with name 
# $1 -> folder path
# $2 -> test file (without extension)
# $3 -> extension of test file
function run_named_eg () {
    run_eg $1 "$2.$3" "generated_$2.bats" "output_$2.txt"
}

# Run example that starts with number order 
# $1 -> folder path
# $2 -> order number
# $3 -> test file (without extension and order number)
# $4 -> extension of test file
function run_numeric_eg () {
    run_eg $1 "$2_$3.$4" "$2_generated_$3.bats" "$2_output_$3.txt"
}


run_named_eg $examples "batspp_example" "batspp"
run_named_eg $examples "bash_example" "bash"
run_numeric_eg $test_cases "1" "no_setup_directive" "batspp"
run_numeric_eg $test_cases "2" "function" "batspp"
run_numeric_eg $test_cases "3" "aliases" "batspp"
run_numeric_eg $test_cases "4" "comments" "batspp"
