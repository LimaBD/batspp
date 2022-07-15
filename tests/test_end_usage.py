#!/usr/bin/env python3
#
# Tests for end usage
#


"""Tests for end usage"""


# Standard packages
import re
import unittest
import os


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import glue_helpers as gh
from mezcla import debug


# Constants
EXAMPLES_PATH = './docs/examples'
# This and "script_module=None" solve problem:
#     "Assertion failed: "No module named" not in help_usage"
BATSPP_PATH = os.path.abspath('./batspp/batspp')


class TestEndUsage(TestWrapper):
    """Class for testcase definition"""
    script_module = None
    maxDiff       = None

    def test_batspp_example(self):
        """End test docs/examples/batspp_example.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_batspp_example(); self={self}")

        actual_filename = f'{self.temp_file}.bats'

        output = gh.run(f'cd {EXAMPLES_PATH} && {BATSPP_PATH} --save {actual_filename} batspp_example.batspp')
        output += '\n' # Compensate the new line added by gh.read_lines()

        # Check output
        expected_output = gh.read_file(f'{EXAMPLES_PATH}/output_batspp_example.txt')
        self.assertEqual(output, expected_output)

        # Check file content
        expected_content = gh.read_file(f'{EXAMPLES_PATH}/generated_batspp_example.bats')
        actual_content = gh.read_file(actual_filename)

        # Manipulate a little the output to make equal the random number
        pattern = r'TEMP_DIR=\"\/tmp\/batspp-(\d+)\"\n'
        random_folder = re.search(pattern, actual_content).group(0)
        expected_content = re.sub(pattern, str(random_folder), expected_content)

        self.assertEqual(actual_content, expected_content)


if __name__ == '__main__':
    unittest.main()
