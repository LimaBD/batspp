#!/bin/bash
#
# Run Batspp and save examples
# output and content
#

examples=$(dirname $(realpath -s $0))
base=$examples/../..

function run_eg () {

    # Args
    filename=$1
    extension=$2

    # Set args to run
    script="python3 $base/batspp/batspp"
    file=$examples/$filename.$extension
    content=$examples/generated_$filename.bats
    output=$examples/output_$1.txt

    # Print trace
    echo ">>>>>>>>>>>>>>>>>>> RUN"
    echo -e "script\t$script"
    echo -e "test file\t$file"
    echo -e "content path\t$content"
    echo -e "output path\t$output\n"

    # Run
    cd $examples
    $script --hexview_debug --save $content $file > $output
}

# Examples
run_eg "batspp_example" "batspp"
run_eg "bash_example" "bash"
