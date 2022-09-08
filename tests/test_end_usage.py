#!/usr/bin/env python3
#
# Tests for Batspp end usage
#
# This install the package/script
# and runs regression tests with
# the docs/examples
#
# These docs/examples generated tests and
# output files can be updated automatically
# running: $ tools/run_examples.bash
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_end_usage.py
#


"""Tests for Batspp end usage"""


# Standard packages
from re import sub as re_sub
from os import path as os_path


# Installed packages
import pytest
from mezcla.unittest_wrapper import TestWrapper
from mezcla import glue_helpers as gh
from mezcla import debug


# Local packages
## NOTE: this is empty for now


# Reference to the module being tested
SCRIPT = 'batspp'


# Constants
TESTS_PATH = os_path.dirname(__file__)
EXAMPLES_PATH = f'{TESTS_PATH}/../docs/examples'
CASES_PATH = f'{TESTS_PATH}/cases'


class TestEndUsage(TestWrapper):
    """Class for testcase definition"""
    script_module = None
    maxDiff = None

    # This avoids install multiples
    # times the same package.
    is_package_installed = False

    def run_regression_test(self, dir_path:str, file: str, extension: str) -> None:
        """
        Run end test FILE with EXTENSION on DIR_PATH,
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

        output = gh.run(f'cd {dir_path} && {SCRIPT} --hexdump_debug --save {actual_filename} ./{file}.{extension}')
        output += '\n' if output else '' # Compensate the new line added by gh.read_lines()

        # Check output
        expected_output = gh.read_file(f'{dir_path}/output_{file}.txt')
        self.assertEqual(output, expected_output)

        # Check file content
        expected_content = gh.read_file(f'{dir_path}/generated_{file}.bats')
        actual_content = gh.read_file(actual_filename)

        # Manipulate a little the output to make equal the random number
        temp_dir_pattern = r'TEMP_DIR=.+'
        actual_content = re_sub(temp_dir_pattern, '', actual_content)
        expected_content = re_sub(temp_dir_pattern, '', expected_content)

        source_pattern = r'source .+'
        actual_content = re_sub(source_pattern, '', actual_content)
        expected_content = re_sub(source_pattern, '', expected_content)

        self.assertEqual(actual_content, expected_content)

    @pytest.mark.slow
    def test_batspp_example(self):
        """End test docs/examples/batspp_example.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_batspp_example(); self={self}")
        self.run_regression_test(dir_path=EXAMPLES_PATH, file='batspp_example', extension='batspp')

    @pytest.mark.slow
    def test_bash_example(self):
        """End test docs/examples/bash_example.bash"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_bash_example(); self={self}")
        self.run_regression_test(dir_path=EXAMPLES_PATH, file='bash_example', extension='bash')

    @pytest.mark.slow
    def test_no_setup_directive(self):
        """End test tests/cases/no_setup_directive.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_no_setup_directive(); self={self}")
        self.run_regression_test(dir_path=CASES_PATH, file='no_setup_directive', extension='batspp')


if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
