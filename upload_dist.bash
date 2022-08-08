#!/bin/bash
#
# Script file to:
# - install and upgrade all required tools
# - install dependencies
# - compile and install package
# - upload dist to PyPi
#


function install_required_tools () {
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
}


function install_dependencies () {
    echo "build - checking dependencies..."
    pip install -r ./requirements.txt
}


# Upload to pypi
#
# $1 -> "test" or "main"
function upload_pypi () {
    echo "build - compiling package..."
    # This will create build, dist and project.egg.info folders
    python3 setup.py bdist_wheel

    echo "build - uploading to PyPi..."

    # Uploading to Test Pypi
    #
    # More information here
    # https://packaging.python.org/en/latest/guides/using-testpypi/
    if [ "$1" == 'main' ]
    then
        twine upload dist/* --verbose
    elif [ "$1" == 'test' ]
    then
        twine upload --repository testpypi dist/* --verbose
    else
        echo "no Pypi main|test selected"
    fi
}


function clean () {
    echo "build - cleaning"
    rm -rf ./build/ ./dist/ ./batspp/batspp.egg-info
}


function main () {
    if [[ "$1" == "main"|| "$1" == "test" ]]
    then
        install_required_tools
        install_dependencies
        upload_pypi "$1"
        clean
    else
        echo 'Upload Batspp dist'
        echo ''
        echo 'Usage:'
        echo "- upload main Pypi: $ $0 main"
        echo "- upload test Pypi: $ $0 test"
        echo ''
    fi
}

main $@
