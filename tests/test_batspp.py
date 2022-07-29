#!/usr/bin/env python3
#
# Tests for batspp script
#


"""Tests for batspp script"""


# Standard packages
import unittest
import os


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import glue_helpers as gh
from mezcla import debug


# This and "script_module=None" solve problem:
#     "Assertion failed: "No module named" not in help_usage"
BATSPP_PATH = os.path.abspath('./batspp/batspp')


class TestBatspp(TestWrapper):
    """Class for testcase definition"""
    script_module     = None
    use_temp_base_dir = True
    maxDiff           = None

    simple_test = ('# Example test\n\n'
                   '$ echo "hello world"\n'
                   'hello world\n\n')

    def test_file(self):
        """Test for test file argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_file({self})")

        self.temp_file += '.batspp'

        gh.write_file(self.temp_file, self.simple_test)
        result = gh.run(f'python3 {BATSPP_PATH} {self.temp_file}')
        self.assertEqual(result, '1..1\nok 1 test of line 3')

    def test_save_path(self):
        """Test for --save_path argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_save_path({self})")

        test_file = f'{self.temp_file}.batspp'
        save_file = f'{self.temp_file}.bats'

        # Generated test with content should be saved
        gh.write_file(test_file, self.simple_test)
        result = gh.run(f'python3 {BATSPP_PATH} --save {save_file} {test_file}')
        self.assertEqual(result, '1..1\nok 1 test of line 3')
        self.assertTrue(gh.read_file(save_file))

        # Generated empty test should not be saved
        another_file = f'{self.temp_file}-another.bats'
        gh.write_file(test_file, '')
        result = gh.run(f'python3 {BATSPP_PATH} --save {another_file} {test_file}')
        self.assertTrue(gh.read_file(save_file)) # File from the last run should keep unmodified
        self.assertFalse(gh.file_exists(another_file))

        # Test argument as enviroment variable
        another_file = f'{self.temp_file}-another1.bats'
        gh.write_file(test_file, self.simple_test)
        result = gh.run(f'SAVE={another_file} python3 {BATSPP_PATH} {test_file}')
        self.assertEqual(result, '1..1\nok 1 test of line 3')
        self.assertTrue(gh.read_file(another_file))

    def test_output(self):
        """Test --output argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_output({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, '')

        # Empty test file
        result = gh.run(f'python3 {BATSPP_PATH} --output {test_file}')
        self.assertTrue(result.startswith('Not founded tests on file'))

        # Test with content
        gh.write_file(test_file, self.simple_test)
        result = gh.run(f'python3 {BATSPP_PATH} --output {test_file}')
        self.assertTrue(result.startswith('#!/usr/bin/env bats'))

        # Test argument as enviroment variable
        result = gh.run(f'OUTPUT=0 python3 {BATSPP_PATH} {test_file}')
        self.assertFalse(result.startswith('#!/usr/bin/env bats'))
        result = gh.run(f'OUTPUT=1 python3 {BATSPP_PATH} {test_file}')
        self.assertTrue(result.startswith('#!/usr/bin/env bats'))

    def test_sources(self):
        """Test --sources argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_sources({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        expected_source = 'source ./some_file_to_load.bash'

        # Test command-line argument
        result = gh.run(f'python3 {BATSPP_PATH} --output --sources ./some_file_to_load.bash {test_file}')
        self.assertTrue(expected_source in result)

        # Test argument as enviroment variable
        result = gh.run(f'SOURCES=./invalid python3 {BATSPP_PATH} --output {test_file}')
        self.assertFalse(expected_source in result)
        result = gh.run(f'SOURCES=./some_file_to_load.bash python3 {BATSPP_PATH} --output {test_file}')
        self.assertTrue(expected_source in result)

    def test_temp_dir(self):
        """Test --temp_dir argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_temp_dir({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        # With temporal dir specified
        result = gh.run(f'python3 {BATSPP_PATH} --output --temp_dir /tmp/temporal_folder/ {test_file}')
        self.assertTrue('TEMP_DIR="/tmp/temporal_folder/"' in result)

        # Not temporal dir specified (uses default /tmp)
        result = gh.run(f'python3 {BATSPP_PATH} --output {test_file}')
        self.assertTrue('TEMP_DIR="/tmp/batspp-' in result)

        # Changind TMP env var
        result = gh.run(f'TMP=/tmp/another/ python3 {BATSPP_PATH} --output {test_file}')
        self.assertTrue('TEMP_DIR="/tmp/another/batspp-' in result)

    def test_copy_dir(self):
        """Test --copy_dir argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_copy_dir({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        expected_constant = 'COPY_DIR="./some/folder/to/copy"'
        expected_command = 'command cp $COPY_DIR '

        # Test command cp on test file
        result = gh.run(f'TMP={self.temp_base}/ python3 {BATSPP_PATH} --copy_dir ./some/folder/to/copy --output {test_file}')
        self.assertTrue(expected_constant in result)
        self.assertTrue(expected_command in result)

        # Test env var
        result = gh.run(f'TMP={self.temp_base}/ COPY_DIR=./some/folder/to/copy python3 {BATSPP_PATH} --output {test_file}')
        self.assertTrue(expected_constant in result)
        self.assertTrue(expected_command in result)

        ## TODO: test copy when running bats

    def test_visible_paths(self):
        """Test --visible_paths argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_visible_paths({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        # A single path
        result = gh.run(f'python3 {BATSPP_PATH} --visible_paths ./some/folder/ --output {test_file}')
        self.assertTrue('# Setup\nPATH=./some/folder/:$PATH\n' in result)

        expected_setup = '# Setup\nPATH=./some/folder/:./another/folder/:$PATH\n'

        # Multiple path
        result = gh.run(f'python3 {BATSPP_PATH} --visible_paths "./some/folder/ ./another/folder/" --output {test_file}')
        self.assertTrue(expected_setup in result)

        # Test env var
        result = gh.run(f'VISIBLE_PATHS="./some/folder/ ./another/folder/" python3 {BATSPP_PATH} --output {test_file}')
        self.assertTrue(expected_setup in result)
        result = gh.run(f'VISIBLE_PATHS="" python3 {BATSPP_PATH} --output {test_file}')
        self.assertFalse(expected_setup in result)

    def test_run_options(self):
        """Test --run_options argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_run_options({self})")
        ## TODO: WORK-IN-PROGRESS

    def test_skip_run(self):
        """Test --skip_run argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_skip_run({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        result = gh.run(f'python3 {BATSPP_PATH} --skip_run {test_file}')
        self.assertFalse(result)
        result = gh.run(f'SKIP_RUN=0 python3 {BATSPP_PATH} {test_file}')
        self.assertTrue(result)
        result = gh.run(f'SKIP_RUN=1 python3 {BATSPP_PATH} {test_file}')
        self.assertFalse(result)

    def test_omit_trace(self):
        """Test --omit_trace argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_omit_trace({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        expected_assert = '# Assertion of line 3\n\t[ "$(test-of-line-3-line3-actual)" == "$(test-of-line-3-line3-expected)" ]'
        expected_function = 'function print_debug() {'

        # Test command-line argument
        result = gh.run(f'python3 {BATSPP_PATH} --output --omit_trace {test_file}')
        self.assertTrue(expected_assert in result)
        self.assertFalse(expected_function in result)

        # Test env var
        result = gh.run(f'OMIT_TRACE=1 python3 {BATSPP_PATH} --output {test_file}')
        self.assertTrue(expected_assert in result)
        self.assertFalse(expected_function in result)

    def test_disable_aliases(self):
        """Test --disable_aliases argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_disable_aliases({self})")
        ## TODO: WORK-IN-PROGRESS

    def test_hexview(self):
        """Test --hexview argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_hexview({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        result = gh.run(f'python3 {BATSPP_PATH} --hexview_debug --output {test_file}')
        self.assertTrue('VERBOSE_DEBUG="| python3 -m hexdump -"' in result)


if __name__ == '__main__':
    unittest.main()
