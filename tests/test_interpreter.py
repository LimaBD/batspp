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
from mezcla import debug


# Local modules
#
# to avoid import errors, must install package with '$ pip install .'
sys.path.insert(0, './../batspp')
from interpreter import NodeVisitor, Interpreter


class TestNodeVisitor(TestWrapper):
    """Class for testcase definition"""
    script_module = TestWrapper.derive_tested_module_name(__file__)
    maxDiff       = None

    ## TODO: implement stub classes to test visitors

    def test_visit(self):
        """Test for visit()"""
        ## TODO: WORK-IN-PROGRESS

    def test_generic_visitor(self):
        """Test for generic_visitor()"""
        ## TODO: WORK-IN-PROGRESS


class TestInterpreter(TestWrapper):
    """Class for testcase definition"""
    script_module = TestWrapper.derive_tested_module_name(__file__)
    maxDiff       = None

    def test_visit_TestsSuite(self):
        """Test for visit_TestsSuite()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Setup(self):
        """Test for visit_Setup()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Test(self):
        """Test for visit_Test()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Assertion(self):
        """Test for visit_Assertion()"""
        ## TODO: WORK-IN-PROGRESS

    def test_interpret(self):
        """Test for interpret()"""
        ## TODO: WORK-IN-PROGRESS


if __name__ == '__main__':
    unittest.main()
