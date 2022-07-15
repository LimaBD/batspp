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
sys.path.insert(0, './batspp')
import exceptions # type: ignore


class TestExceptions(TestWrapper):
    """Class for testcase definition"""
    script_module = None
    maxDiff       = None

    def test_error(self):
        """Test for error()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestExceptions.test_error(); self={self}")
        ## TODO: WORK-IN-PROGRESS


if __name__ == '__main__':
    unittest.main()
