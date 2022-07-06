#!/usr/bin/env python3
#
# Tests for batspp script
#


"""Tests for batspp script"""


# Standard packages
import unittest


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import glue_helpers as gh
from mezcla import debug


class TestBatspp(TestWrapper):
    """Class for testcase definition"""
    script_module     = f'./batspp/{TestWrapper.derive_tested_module_name(__file__)}'
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
        result = gh.run(f'python3 {self.script_module} {self.temp_file}')
        self.assertEqual(result, '1..1\nok 1 test of line 3')

    def test_save_path(self):
        """Test for --save_path argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_save_path({self})")

        test_file = f'{self.temp_file}.batspp'
        save_file = f'{self.temp_file}.bats'

        # Generated test with content should be saved
        gh.write_file(test_file, self.simple_test)
        result = gh.run(f'python3 {self.script_module} --save {save_file} {test_file}')
        self.assertEqual(result, '1..1\nok 1 test of line 3')
        self.assertTrue(gh.read_file(save_file))

        # Generated empty test should not be saved
        another_file = f'{self.temp_file}-another.bats'
        gh.write_file(test_file, '')
        result = gh.run(f'python3 {self.script_module} --save {another_file} {test_file}')
        self.assertTrue(gh.read_file(save_file)) # File from the last run should keep unmodified
        self.assertFalse(gh.read_file(another_file))

    def test_output(self):
        """Test --output argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_output({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, '')

        # Empty test file
        result = gh.run(f'python3 {self.script_module} --output {test_file}')
        self.assertTrue(result.startswith('Not founded tests on file'))

        # Test with content
        gh.write_file(test_file, self.simple_test)
        result = gh.run(f'python3 {self.script_module} --output {test_file}')
        self.assertTrue(result.startswith('#!/usr/bin/env bats'))

    def test_sources(self):
        """Test --sources argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_sources({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        result = gh.run(f'python3 {self.script_module} --output --sources ./some_file_to_load.bash {test_file}')
        self.assertTrue('source ./some_file_to_load.bash' in result)

    def test_temp_dir(self):
        """Test --temp_dir argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_temp_dir({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        # With temporal dir specified
        result = gh.run(f'python3 {self.script_module} --output --temp_dir /tmp/temporal_folder/ {test_file}')
        self.assertTrue('TEMP_DIR="/tmp/temporal_folder/"' in result)

        # Not temporal dir specified (uses default /tmp)
        result = gh.run(f'python3 {self.script_module} --output {test_file}')
        self.assertTrue('TEMP_DIR="/tmp/batspp-' in result)

        # Changind TMP env var
        result = gh.run(f'TMP=/tmp/another/ python3 {self.script_module} --output {test_file}')
        self.assertTrue('TEMP_DIR="/tmp/another/batspp-' in result)

    def test_copy_dir(self):
        """Test --copy_dir argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_copy_dir({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        # Test command cp on test file
        result = gh.run(f'TMP={self.temp_base}/ python3 {self.script_module} --copy_dir ./some/folder/to/copy --output {test_file}')
        self.assertTrue('COPY_DIR="./some/folder/to/copy"' in result)
        self.assertTrue('command cp $COPY_DIR ' in result)

        ## TODO: test copy when running bats

    def test_visible_path(self):
        """Test --visible_path argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_visible_path({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        # A single path
        result = gh.run(f'python3 {self.script_module} --visible_path ./some/folder/ --output {test_file}')
        self.assertTrue('# Setup\nPATH=./some/folder/:$PATH\n' in result)

        # Multiple path
        result = gh.run(f'python3 {self.script_module} --visible_path "./some/folder/ ./another/folder/" --output {test_file}')
        self.assertTrue('# Setup\nPATH=./some/folder/:./another/folder/:$PATH\n' in result)

    def test_run_options(self):
        """Test --run_options argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_run_options({self})")
        ## TODO: WORK-IN-PROGRESS

    def test_skip_run(self):
        """Test --skip_run argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_skip_run({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        result = gh.run(f'python3 {self.script_module} --skip_run {test_file}')
        self.assertFalse(result)

    def test_omit_trace(self):
        """Test --omit_trace argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_omit_trace({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        result = gh.run(f'python3 {self.script_module} --output --omit_trace {test_file}')
        self.assertTrue('# Assertion of line 3\n\t[ "$(test-of-line-3-line3-actual)" == "$(test-of-line-3-line3-expected)" ]' in result)
        self.assertFalse('function print_debug() {' in result)

    def test_disable_aliases(self):
        """Test --disable_aliases argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_disable_aliases({self})")
        ## TODO: WORK-IN-PROGRESS


if __name__ == '__main__':
    unittest.main()
