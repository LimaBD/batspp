#!/usr/bin/env python3
#
# Tests for _exceptions module
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_exceptions.py
#


"""Tests for _exceptions module"""


# Standard packages
from sys import path as sys_path


# Installed packages
import pytest
from mezcla.unittest_wrapper import TestWrapper
from mezcla import debug


# Local packages
sys_path.insert(0, './batspp')


# Reference to the module being tested
import batspp._exceptions as THE_MODULE


class TestExceptions:
    """Class for testcase definition"""

    def test_error(self):
        """Test for error()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestExceptions.test_error(); self={self}")
        ## TODO: WORK-IN-PROGRESS


if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
