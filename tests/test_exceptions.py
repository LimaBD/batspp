#!/usr/bin/env python3
#
# Tests for exceptions.py module
#


"""Tests for exceptions.py module"""


# Standard packages
import sys
import unittest


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import debug


# Module being tested
#
# to avoid import errors, must install package with '$ pip install .'
sys.path.insert(0, './../batspp')
import exceptions


class TestExceptions(TestWrapper):
    """Class for testcase definition"""
    script_module = TestWrapper.derive_tested_module_name(__file__)
    maxDiff       = None

    def test_error(self):
        """Test for error()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestExceptions.test_error(); self={self}")
        ## TODO: WORK-IN-PROGRESS


if __name__ == '__main__':
    unittest.main()
