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

    def run_regression_test(
            self,
            dir_path: str,
            test_file: str, extension: str,
            generated_file: str,
            output_file: str,
            ) -> None:
        """
        Run end TEST_FILE with EXTENSION on DIR_PATH and
        check actual and expected GENERATED_FILE and OUTPUT_FILE,
        this installs Batspp package using pip
        """
        debug.trace(debug.QUITE_DETAILED,
                    f"TestEndUsage.run_example(); self={self}")

        # Check installation of Batspp
        if not self.is_package_installed:
            print(
                '=========== installing ==========='
                f'{gh.run("pip install .")}'
                '==================================\n'
                )
            self.is_package_installed = True

        # Run Batspp
        temp_filename = f'{self.temp_file}.bats'
        actual_output = gh.run(f'cd {dir_path} && {SCRIPT} --hexdump_debug --save {temp_filename} ./{test_file}.{extension}')
        assert actual_output
        actual_generated = gh.read_file(temp_filename)[:-1]
        assert actual_generated

        # Get expected values
        expected_generated = gh.read_file(f'{dir_path}/{generated_file}.bats')[:-1]
        expected_output = gh.read_file(f'{dir_path}/{output_file}.txt')[:-1]

        # Make equal the random number and paths
        pattern_to_ignore = r'(TEMP_DIR=.+|source .+|.*\/tmp\/.+)'
        actual_generated = re_sub(pattern_to_ignore, '', actual_generated)
        actual_output = re_sub(pattern_to_ignore, '', actual_output)
        expected_generated = re_sub(pattern_to_ignore, '', expected_generated)
        expected_output = re_sub(pattern_to_ignore, '', expected_output)

        assert actual_generated == expected_generated
        assert actual_output == expected_output

    @pytest.mark.sudo
    @pytest.mark.reinstall
    def test_batspp_example(self):
        """End test docs/examples/batspp_example.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestEndUsage.test_batspp_example(); self={self}")
        self.run_regression_test(
            dir_path=EXAMPLES_PATH,
            test_file='batspp_example', extension='batspp',
            generated_file='generated_batspp_example',
            output_file='output_batspp_example'
            )

    @pytest.mark.sudo
    @pytest.mark.reinstall
    def test_bash_example(self):
        """End test docs/examples/bash_example.bash"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestEndUsage.test_bash_example(); self={self}")
        self.run_regression_test(
            dir_path=EXAMPLES_PATH,
            test_file='bash_example', extension='bash',
            generated_file='generated_bash_example',
            output_file='output_bash_example'
            )

    @pytest.mark.reinstall
    def test_no_setup_directive(self):
        """End test tests/cases/1_no_setup_directive.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTestEndUsageInterpreter.test_no_setup_directive(); self={self}")
        self.run_regression_test(
            dir_path=CASES_PATH,
            test_file='1_no_setup_directive', extension='batspp',
            generated_file='1_generated_no_setup_directive',
            output_file='1_output_no_setup_directive'
            )

    @pytest.mark.reinstall
    def test_function(self):
        """End test tests/cases/2_function.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestEndUsage.test_function(); self={self}")
        self.run_regression_test(
            dir_path=CASES_PATH,
            test_file='2_function', extension='batspp',
            generated_file='2_generated_function',
            output_file='2_output_function'
            )

    @pytest.mark.reinstall
    def test_aliases(self):
        """End test tests/cases/2_aliases.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestEndUsage.test_aliases(); self={self}")
        self.run_regression_test(
            dir_path=CASES_PATH,
            test_file='3_aliases', extension='batspp',
            generated_file='3_generated_aliases',
            output_file='3_output_aliases'
            )

    @pytest.mark.reinstall
    def test_comments(self):
        """End test tests/cases/4_comments.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestEndUsage.test_comments(); self={self}")
        self.run_regression_test(
            dir_path=CASES_PATH,
            test_file='4_comments', extension='batspp',
            generated_file='4_generated_comments',
            output_file='4_output_comments'
            )

    @pytest.mark.reinstall
    def test_long_outputs(self):
        """End test tests/cases/5_long_outputs.batspp"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestEndUsage.test_comments(); self={self}")
        self.run_regression_test(
            dir_path=CASES_PATH,
            test_file='5_long_outputs', extension='batspp',
            generated_file='5_generated_long_outputs',
            output_file='5_output_long_outputs'
            )

if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
