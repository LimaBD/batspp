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
        """Test for save argument"""
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
        """Test output argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_output({self})")

        test_file = f'{self.temp_file}.batspp'

        # Empty test file
        gh.write_file(test_file, '')
        result = gh.run(f'python3 {self.script_module} --output {test_file}')
        self.assertTrue(result.startswith('Not founded tests on file'))

        # Test with content
        gh.write_file(test_file, self.simple_test)
        result = gh.run(f'python3 {self.script_module} --output {test_file}')
        self.assertTrue(result.startswith('#!/usr/bin/env bats'))

    def test_source(self):
        """Test source argument"""

        test_file = f'{self.temp_file}.batspp'

        gh.write_file(test_file, self.simple_test)
        result = gh.run(f'python3 {self.script_module} --output --source ./some_file_to_load.bash {test_file}')
        self.assertTrue('source ./some_file_to_load.bash' in result)


if __name__ == '__main__':
    unittest.main()
