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
python3 -m pip install --upgrade build

# Setuptools is a package development process library designed
# for creating and distributing Python packages.
sudo python3 -m pip install --upgrade pip setuptools

# The Wheel package provides a bdist_wheel command for setuptools.
# It creates .whl file which is directly installable through the pip install command.
sudo python3 -m pip install --upgrade wheel

# This is a smart progress meter used internally by Twine.
sudo python3 -m pip install --upgrade tqdm

# The Twine package provides a secure, authenticated,
# and verified connection between your system and PyPi over HTTPS.
sudo python3 -m pip install --upgrade twine

echo "build - checking dependencies..."
pip install mezcla
pip install -r ./submodules/mezcla/requirements.txt

echo "build - compiling package..."
# This will create build, dist and project.egg.info folders
python3 setup.py bdist_wheel

echo "build - installing locally..."
version=$(python3 -c 'from batspp.version import __version__; print(__version__)' | sed 's/\./-/g')
python3 -m pip install dist/batspp-$version-py3-none-any.whl

echo "build - uploading dist/* to PyPi..."
python3 -m twine upload dist/* --verbose

echo "build - finish!"
