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


# Constants
EXAMPLES_PATH = './docs/examples'


class TestEndUsage(TestWrapper):
    """Class for testcase definition"""
    script_module = 'batspp'
    maxDiff       = None

    def test_batspp_example(self):
        """End test docs/examples/batspp_example.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_batspp_example(); self={self}")

        actual_filename = f'{self.temp_file}.bats'

        output = gh.run(f'cd {EXAMPLES_PATH} && {self.script_module} --save {actual_filename} batspp_example.batspp')

        # New line is added to compensate the new line added by gh.read_lines()
        output += '\n'

        # Check output
        expected_output = gh.read_file(f'{EXAMPLES_PATH}/output_batspp_example.txt')
        self.assertEqual(output, expected_output)

        # Check file content
        expected_content = gh.read_file(f'{EXAMPLES_PATH}/generated_batspp_example.bats')
        self.assertEqual(gh.read_file(actual_filename), expected_content)


if __name__ == '__main__':
    unittest.main()
