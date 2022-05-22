#!/bin/bash
#
# TODO: description
#


echo "build - checking the required tools..."

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


echo "build - compiling package..."
# This will create build, dist and project.egg.info folders
python3 setup.py bdist_wheel


## TODO: add args to choose between locally, TestPyPi or PyPi


echo "build - installing locally..."
## TODO: automate version update
python3 -m pip install dist/batspp-1.1.0-py3-none-any.whl


echo "build - uploading dist/* to PyPi..."
## TODO: add exception if this fails
python3 -m twine upload dist/* --verbose


echo "build - installing from Pypi..."


## TODO: clean files after installation


echo "build - finish!"
