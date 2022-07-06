#!/bin/bash
#
# Run Batspp and save examples
#

ABS_PATH=$(dirname $(realpath -s $0))

cd $ABS_PATH # Avoid problems with tests references to another files

FILE="batspp_example"
batspp --save $ABS_PATH/generated_$FILE.bats $ABS_PATH/$FILE.batspp > $ABS_PATH/output_$FILE.txt
