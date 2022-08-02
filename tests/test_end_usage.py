#!/usr/bin/env python3
#
# Tests for Batspp end usage
#
# Thins install the package/script
# and runs regression tests with
# the docs/examples
#
# These docs/examples generated tests and
# output files can be updated automatically
# running: $ docs/examples/run_examples.bash
#


"""Tests for Batspp end usage"""


# Standard packages
import re
import unittest
import os


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import glue_helpers as gh
from mezcla import debug


# Constants
EXAMPLES_PATH = os.path.dirname(__file__) + '/../docs/examples'
SCRIPT = 'batspp'


class TestEndUsage(TestWrapper):
    """Class for testcase definition"""
    script_module = None
    maxDiff       = None

    # This avoids install multiples
    # times the same package.
    is_package_installed = False

    def run_test_example(self, file: str, extension: str) -> None:
        """
        Run end test FILE example,
        this installs Batspp package using pip
        """
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.run_example(); self={self}")

        actual_filename = f'{self.temp_file}.bats'

        if not self.is_package_installed:
            print(
                '=========== installing ==========='
                f'{gh.run("pip install .")}'
                '==================================\n'
            )
            self.is_package_installed = True

        output = gh.run(f'cd {EXAMPLES_PATH} && {SCRIPT} --hexdump_debug --save {actual_filename} ./{file}.{extension}')
        output += '\n' if output else '' # Compensate the new line added by gh.read_lines()

        # Check output
        expected_output = gh.read_file(f'{EXAMPLES_PATH}/output_{file}.txt')
        self.assertEqual(output, expected_output)

        # Check file content
        expected_content = gh.read_file(f'{EXAMPLES_PATH}/generated_{file}.bats')
        actual_content = gh.read_file(actual_filename)

        # Manipulate a little the output to make equal the random number
        pattern = r'TEMP_DIR=\"\/tmp\/batspp-(\d+)\"\n'
        random_folder = re.search(pattern, actual_content).group(0)
        expected_content = re.sub(pattern, str(random_folder), expected_content)

        self.assertEqual(actual_content, expected_content)

    def test_batspp_example(self):
        """End test docs/examples/batspp_example.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_batspp_example(); self={self}")
        self.run_test_example(file='batspp_example', extension='batspp')

    def test_bash_example(self):
        """End test docs/examples/bash_example.bash"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_bash_example(); self={self}")
        self.run_test_example(file='bash_example', extension='bash')


if __name__ == '__main__':
    unittest.main()
