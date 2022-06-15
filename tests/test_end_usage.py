#!/usr/bin/env python3
#
# Tests for end usage
#


"""Tests for end usage"""


# Standard packages
import unittest


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import glue_helpers as gh
from mezcla import debug


class TestEndUsage(TestWrapper):
    """Class for testcase definition"""
    script_module = f'./batspp/{TestWrapper.derive_tested_module_name(__file__)}'
    maxDiff       = None

    ## TODO: WORK-IN-PROGRESS


if __name__ == '__main__':
    unittest.main()
