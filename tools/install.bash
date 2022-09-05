#!/bin/bash
#
# Install Batspp and its depedencies
#

base="$(dirname $(realpath -s $0))/.."

pip install -r $base/requirements/development.txt
pip install -r $base/requirements/production.txt
pip install $base
