#!/usr/bin/env python3
#
# Tests for _ipynb_to_batspp module
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_ipynb_to_batspp.py
#

"""Tests for _ipynb_to_batspp module"""

# Standard packages
from sys import path as sys_path

# Installed packages
import pytest
from mezcla.unittest_wrapper import TestWrapper
from mezcla import debug

# Local packages
sys_path.insert(0, './batspp')

# Reference to the module being tested
import batspp._ipynb_to_batspp as THE_MODULE

class TestIpynbToBatspp:
    """Class for testcase definition"""

    ## TODO: WORK-IN-PROGRESS

if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
