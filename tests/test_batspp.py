#!/usr/bin/env python3
#
# Tests for batspp script
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_batspp.py
#
# TODO: implement TestWrapper.run_script() to get coverage of tested subprocess
#


"""Tests for batspp script"""


# Standard packages
from os import (
    path as os_path,
    makedirs as os_makedirs,
    )

# Installed packages
import pytest
from mezcla.unittest_wrapper import TestWrapper
from mezcla import glue_helpers as gh
from mezcla import debug
from mezcla import system

# Local packages
## NOTE: this is empty for now


# Reference to the module being tested
#
# This and "script_module=None" solve problem:
#     "Assertion failed: "No module named" not in help_usage"
BATSPP_PATH = os_path.abspath('./batspp/batspp')


class TestBatspp(TestWrapper):
    """Class for testcase definition"""
    script_module     = None
    use_temp_base_dir = True
    maxDiff           = None

    simple_test = (
        '# Example test\n\n'
        '$ echo "hello world"\n'
        'hello world\n\n'
        )

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
        output_file = f'{self.temp_file}.bats'

        # Generated test with content should be saved
        gh.write_file(test_file, self.simple_test)
        gh.run(f'python3 {BATSPP_PATH} --save {output_file} {test_file}')
        self.assertTrue('echo "hello world"' in gh.read_file(output_file))

        # Test argument as enviroment variable
        output_file = f'{gh.get_temp_file()}.bats'
        gh.write_file(test_file, self.simple_test)
        gh.run(f'SAVE="{output_file}" python3 {BATSPP_PATH} {test_file}')
        self.assertTrue('echo "hello world"' in gh.read_file(output_file))

        # Dir paths should have a default file name
        test_file = gh.get_temp_file()
        save_dir_path = '/tmp/'
        gh.write_file(test_file + '.batspp', self.simple_test)
        gh.run(f'python3 {BATSPP_PATH} --save {save_dir_path} {test_file}.batspp')
        output_file = f'{save_dir_path}generated_{gh.basename(test_file)}.bats'
        self.assertTrue('echo "hello world' in gh.read_file(output_file))

    def test_output(self):
        """Test --output argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_output({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, '')

        # Empty test file
        ## TODO: catching of exceptions need to be moodified, hide python traceback
        ## result = gh.run(f'python3 {BATSPP_PATH} --output {test_file}')
        ## self.assertTrue('Not founded tests on file' in result)

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
        self.assertTrue('PATH=./some/folder/:$PATH\n' in result)

        expected_setup = 'PATH=./some/folder/:./another/folder/:$PATH\n'

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

        expected_assert = '# Assertion of line 3\n\tshopt -s expand_aliases\n\t[ "$(echo "hello world")" == "$(echo -e \'hello world\')" ]'
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

    def test_hexdump(self):
        """Test --hexdump argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_hexdump({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        result = gh.run(f'python3 {BATSPP_PATH} --hexdump_debug --output {test_file}')
        self.assertTrue('VERBOSE_DEBUG="| hexdump -C"' in result)

    def test_debug(self):
        """Test --debug argument"""
        debug.trace(debug.DETAILED, f"TestBatspp.test_debug({self})")

        test_file = f'{self.temp_file}.batspp'
        gh.write_file(test_file, self.simple_test)

        result = gh.run(f'python3 {BATSPP_PATH} --debug "| wc -l" --output {test_file}')
        self.assertTrue('VERBOSE_DEBUG="| wc -l"' in result)


if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
