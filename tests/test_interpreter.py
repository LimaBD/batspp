#!/usr/bin/env python3
#
# Tests for interpreter.py module
#


"""Tests for interpreter.py module"""


# Standard packages
import sys
import unittest


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import glue_helpers as gh
from mezcla import debug


# Module being tested
sys.path.insert(0, './../batspp')
import interpreter


class TestIt(TestWrapper):
    """Class for testcase definition"""
    script_module = TestWrapper.derive_tested_module_name(__file__)
    maxDiff       = None


    ## TODO: WORK-IN-PROGRESS


if __name__ == '__main__':
    unittest.main()
