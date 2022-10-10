#!/usr/bin/env python3
#
# Tests for batspp_test module
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_batspp_test.py
#


"""Tests for batspp_test module"""


# Standard packages
from sys import path as sys_path

# Installed packages
import pytest
from mezcla import debug
from mezcla import glue_helpers as gh

# Local packages
sys_path.insert(0, './batspp')
## NOTE: this is empty for now


# Reference to the module being tested
import batspp.batspp_test as THE_MODULE


class TestBatssTest:
    """Class for testcase definition"""

    simple_test = (
        '# Example test\n\n'
        '$ echo "hello world"\n'
        'hello world\n\n'
        )

    def test_transpile_to_bats(self):
        """Ensure transpile_to_bats works as expected"""
        temp_file = f'{gh.get_temp_file()}.batspp'
        gh.write_file(temp_file, self.simple_test)
        batspp_test = THE_MODULE.BatsppTest()
        result = batspp_test.transpile_to_bats(temp_file)
        assert '@test' in result
        assert 'echo "hello world"' in result

    def test_transpile_and_save_bats(self):
        """Ensure transpile_and_save_bats works as expected"""
        input_temp_file = f'{gh.get_temp_file()}.batspp'
        gh.write_file(input_temp_file, self.simple_test)
        output_temp_file = f'{gh.get_temp_file()}.bats'
        batspp_test = THE_MODULE.BatsppTest()
        batspp_test.transpile_and_save_bats(input_temp_file, output_temp_file)
        result = gh.read_file(output_temp_file)
        assert '@test' in result
        assert 'echo "hello world"' in result

    def test_run(self):
        """Ensure run works as expected"""
        temp_file = f'{gh.get_temp_file()}.batspp'
        gh.write_file(temp_file, self.simple_test)
        batspp_test = THE_MODULE.BatsppTest()
        result = batspp_test.run(temp_file)
        assert '1..1\nok 1 test of line 3' == result

    def test_add_prefix_to_filename(self):
        """Ensure add_prefix_to_filename works as expected"""
        filename = '/example/some/file.txt'
        result = THE_MODULE.add_prefix_to_filename(filename, 'generated_')
        assert result == '/example/some/generated_file.txt'

    def test_merge_filename_into_path(self):
        """Ensure merge_filename_into_path works as expected"""
        filename = '/example/some/file.txt'
        path = '/another/folder/'
        result = THE_MODULE.merge_filename_into_path(filename, path)
        assert result == '/another/folder/file.txt'

    def test_replace_extension(self):
        """Ensure replace_extension works as expected"""
        filename = '/example/some/file.txt'
        result = THE_MODULE.replace_extension(filename, 'batspp')
        assert result == '/example/some/file.batspp'


if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
