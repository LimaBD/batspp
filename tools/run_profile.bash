#!/bin/bash
#
# Generate performance profile
#

base="$(dirname $(realpath -s $0))/../"
script="$base/batspp/batspp"
examples="$base/docs/examples"

python -m cProfile -s 'cumulative' $script --skip_run $examples/batspp_example.batspp
