#!/bin/bash
#
# Build the documentation for the project using Sphinx.
#

tools=$(dirname $(realpath -s $0))
base=$tools/..
docs=$base/docs/

make -C $docs html
open $docs/build/html/index.html
