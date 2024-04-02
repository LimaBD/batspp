#!/usr/bin/env python3
#
# Tests for _interpreter module
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_interpreter.py
#

"""Tests for _interpreter module"""

# Standard packages
from sys import path as sys_path

# Installed packages
import pytest
from mezcla.unittest_wrapper import TestWrapper
from mezcla import debug

# Local packages
sys_path.insert(0, './batspp')
from batspp._token import (
    TokenData, EOF, SETUP,
    PESO,
    )
from batspp._ast_node import (
    TestSuite, GlobalSetup, GlobalTeardown,
    Test, StandaloneCommands, Command,
    TestReference, Assertion, CommandAssertion,
    SetupAssertion,
    )

# Reference to the module being tested
from batspp._bats_interpreter import bats_interpreter

class TestNodeVisitor:
    """Class for testcase definition"""

    ## TODO: implement stub classes to test visitors

    def test_visit(self):
        """Test for visit()"""
        ## TODO: WORK-IN-PROGRESS

    def test_generic_visitor(self):
        """Test for generic_visitor()"""
        ## TODO: WORK-IN-PROGRESS

class TestInterpreter:
    """Class for testcase definition"""

    def test_visit_TestSuite(self):
        """Test for visit_TestSuite()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_GlobalSetup(self):
        """Test for visit_GlobalSetup()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_GlobalTeardown(self):
        """Test for visit_GlobalTeardown()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Test(self):
        """Test for visit_Test()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Setup(self):
        """Test for visit_Setup()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_StandaloneCommands(self):
        """Test for visit_StandaloneCommands()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_SetupAssertion(self):
        """Test for visit_SetupAssertion()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Assertion(self):
        """Test for visit_Assertion()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_CommandAssertion(self):
        """Test for visit_CommandAssertion()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Command(self):
        """Test for visit_Command()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_CommandExtension(self):
        """Test for visit_CommandExtension()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_ArrowAssertion(self):
        """Test for visit_ArrowAssertion()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_MultilineText(self):
        """Test for visit_MultilineText()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Constants(self):
        """Test for visit_Constants()"""
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Text(self):
        """Test for visit_Text()"""
        ## TODO: WORK-IN-PROGRESS

if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
