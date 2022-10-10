#!/bin/bash
#
# Script file to:
# - install and upgrade all required tools
# - install dependencies
# - compile and install package
# - upload dist to PyPi
#


base=$(dirname $(realpath -s $0))/..


function install_dependencies () {
    echo "==========================> build - checking dependencies... <=========================="
    pip install -r $base/requirements/development.txt
    pip install -r $base/requirements/production.txt
}


# Upload to pypi
#
# $1 -> "test" or "main"
function upload_pypi () {
    echo "==========================> build - compiling package... <=========================="
    # This will create build, dist and project.egg.info folders
    python3 $base/setup.py bdist_wheel

    echo "==========================> build - uploading to PyPi... <=========================="

    # Uploading to Test Pypi
    #
    # More information here
    # https://packaging.python.org/en/latest/guides/using-testpypi/
    if [ "$1" == 'main' ]
    then
        twine upload $base/dist/* --verbose
    elif [ "$1" == 'test' ]
    then
        twine upload --repository testpypi $base/dist/* --verbose
    else
        echo "no Pypi main|test selected"
    fi
}


function clean () {
    echo "==========================> build - cleaning <=========================="
    rm -rf $base/build/ $base/dist/ $base/batspp/batspp.egg-info
}


function main () {
    if [[ "$1" == "main"|| "$1" == "test" ]]
    then
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

cd $base
main $@
