#!/bin/bash
#
# Script file to:
# - install and upgrade all required tools
# - install dependencies
# - compile and install package
# - upload dist to PyPi
#

echo "build - checking the required tools..."

# Make sure your build tool is up to date
pip install build

# Setuptools is a package development process library designed
# for creating and distributing Python packages.
pip install setuptools

# The Wheel package provides a bdist_wheel command for setuptools.
# It creates .whl file which is directly installable through the pip install command.
pip install wheel

# This is a smart progress meter used internally by Twine.
pip install tqdm

# The Twine package provides a secure, authenticated,
# and verified connection between your system and PyPi over HTTPS.
pip install twine

echo "build - checking dependencies..."
pip install -r ./requirements.txt

echo "build - compiling package..."
# This will create build, dist and project.egg.info folders
python3 setup.py bdist_wheel

echo "build - uploading dist/* to PyPi..."
twine upload dist/* --verbose

echo "build - cleaning"
rm -rf ./build/ ./dist/ ./batspp/batspp.egg-info

echo "build - finish!"
