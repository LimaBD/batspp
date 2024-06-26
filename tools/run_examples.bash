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

    # Set runner if passed
    runner="bats"
    if [ ! -z "$5" ]; then
        runner=$5
    fi

    # Set args to run
    script="python3 $base/batspp/batspp"
    test_file=$folder/$test_file
    generated=$folder/$generated.$runner
    output=$folder/$output

    # Print trace
    echo ">>>>>>>>>>>>>>>>>>> RUN"
    echo -e "script\t$script"
    echo -e "test test_file\t$test_file"
    echo -e "generated path\t$generated"
    echo -e "output path\t$output\n"

    # Run
    cd $folder
    $script --hexdump_debug --runner $runner --save $generated $test_file > $output

    # Replace random generated values
    # to avoid changes on git diff
    to_replace="TEMP_DIR=\"\/tmp\/batspp-.*\""
    replacement="TEMP_DIR=\"\/tmp\/batspp-'<REPLACED>'\""
    sed -i "s/$to_replace/$replacement/g" $generated
    # Replace local paths
    to_replace="source .*"
    replacement="source '<REPLACED>'"
    sed -i "s/$to_replace/$replacement/g" $generated
    # Replace random temporal files
    to_replace="\/tmp\/.*"
    replacement="\/tmp\/'<REPLACED>'"
    sed -i "s/$to_replace/$replacement/g" $output
}

# Run example that starts with name 
# $1 -> folder path
# $2 -> test file (without extension)
# $3 -> extension of test file
function run_named_eg () {
    run_eg $1 "$2.$3" "generated_$2" "output_$2.txt"
}

# Run example that starts with number order 
# $1 -> folder path
# $2 -> order number
# $3 -> test file (without extension and order number)
# $4 -> extension of test file
# $5 -> runner, bats by default
function run_numeric_eg () {
    run_eg $1 "$2_$3.$4" "$2_generated_$3" "$2_output_$3.txt" $5
}


run_named_eg $examples "batspp_example" "batspp"
run_named_eg $examples "bash_example" "bash"
run_numeric_eg $test_cases "1" "no_setup_directive" "batspp"
run_numeric_eg $test_cases "2" "function" "batspp"
run_numeric_eg $test_cases "3" "aliases" "batspp"
run_numeric_eg $test_cases "4" "comments" "batspp"
run_numeric_eg $test_cases "5" "long_outputs" "batspp"
run_numeric_eg $test_cases "6" "jupyter_dummy_test" "ipynb"
run_numeric_eg $test_cases "7" "global_setup" "batspp"
