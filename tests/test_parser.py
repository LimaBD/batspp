#!/usr/bin/env python3
#
# Tests for _parser module
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_parser.py
#

"""Tests for _parser module"""

# Standard packages
from sys import path as sys_path

# Installed packages
import pytest
from mezcla import debug

# Local packages
sys_path.insert(0, './batspp')

# Reference to the module being tested
from batspp._parser import _Rule

class TestRule:
    """Class for testcase definition"""

    def test_expect(self):
        """Test for expect() rule method"""
        ## TODO: implement

    def test_optionally(self):
        """Test for optionally() rule method"""
        ## TODO: implement

    def test_zero_or_more(self):
        """Test for zero_or_more() rule method"""
        ## TODO: implement

    def test_one_or_more(self):
        """Test for one_or_more() rule method"""
        ## TODO: implement

    def test_ignore_next(self):
        """Test for ignore_next() rule method"""
        ## TODO: implement

    def test_until(self):
        """Test for until() rule method"""
        ## TODO: implement

    def test_build_tree_from(self):
        """Test for build_tree_from() rule method"""
        ## TODO: implement

if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
