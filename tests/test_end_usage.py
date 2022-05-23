#!/usr/bin/env python3
#
# Tests for end usage
#


"""Tests for end usage"""


# Standard packages
import sys
import unittest


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import glue_helpers as gh
from mezcla import debug


# Module being tested
sys.path.insert(0, './../batspp')


class TestIt(TestWrapper):
    """Class for testcase definition"""
    maxDiff = None


    ## TODO: WORK-IN-PROGRESS


if __name__ == '__main__':
    unittest.main()
