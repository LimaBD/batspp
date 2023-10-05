#!/usr/bin/env python3
#
# Tests for _semantic_analizer module
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_semantic_analizer.py
#

"""Tests for _semantic_analizer module"""

# Standard packages
from sys import path as sys_path

# Installed packages
import pytest
from mezcla import debug

# Local packages
sys_path.insert(0, './batspp')

# Reference to the module being tested
import batspp._exceptions as THE_MODULE

class TestSemanticAnalizer:
    """Class for testcase definition"""

    ## TODO: WORK-IN-PROGRESS

if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
