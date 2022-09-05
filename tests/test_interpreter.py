#!/usr/bin/env python3
#
# Tests for _interpreter module
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_interpreter.py
#


"""Tests for _interpreter module"""


# Standard packages
from sys import path as sys_path


# Installed packages
import pytest
from mezcla.unittest_wrapper import TestWrapper
from mezcla import debug


# Local packages
sys_path.insert(0, './batspp')
from batspp._token import TokenData
from batspp._ast_nodes import (
    AssertionType, Assertion,
    Test, TestsSuite,
    )


# Reference to the module being tested
import batspp._interpreter as THE_MODULE


class TestNodeVisitor:
    """Class for testcase definition"""

    ## TODO: implement stub classes to test visitors

    def test_visit(self):
        """Test for visit()"""
        ## TODO: WORK-IN-PROGRESS

    def test_generic_visitor(self):
        """Test for generic_visitor()"""
        ## TODO: WORK-IN-PROGRESS


class TestInterpreter:
    """Class for testcase definition"""

    def test_visit_TestsSuite(self):
        """Test for visit_TestsSuite()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_visit_TestsSuite(); self={self}")
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Test(self):
        """Test for visit_Test()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_visit_Test(); self={self}")
        data = TokenData(text_line='some line', line=3, column=3)
        interpreter = THE_MODULE.Interpreter()

        interpreter.stack_functions = [
            'function some_function() ...',
            'function another_function() ...',
            ]
        node = Test(pointer='important test', assertions=[], data=data)
        actual = interpreter.visit_Test(node)

        assert interpreter.last_title == 'important test'
        assert '@test "important test"' in actual

        # Check functions
        assert not interpreter.stack_functions
        assert 'function some_function() ...' in actual
        assert 'function another_function() ...' in actual

    def test_visit_Assertion(self):
        """Test for visit_Assertion()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_visit_Assertion(); self={self}")
        data = TokenData(text_line='some line', line=3, column=3)
        interpreter = THE_MODULE.Interpreter()

        interpreter.last_title = 'important test'
        node = Assertion(
            atype=AssertionType.EQUAL,
            actual='echo "some text"',
            expected='some text',
            data=data,
            )
        actual = interpreter.visit_Assertion(node)

        assert len(interpreter.stack_functions) == 2
        assert 'echo "some text"' in interpreter.stack_functions[0]
        assert 'some text' in interpreter.stack_functions[1]

        actual_assertion = actual.splitlines()[-1]
        assert actual_assertion.startswith('\t[ ')
        assert ' == ' in actual_assertion
        assert actual_assertion.endswith(' ]')
        assert interpreter.debug_required

    def test_interpret(self):
        """Test for interpret()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_interpret(); self={self}")
        data = TokenData(text_line='some line', line=3, column=3)

        first_assertion = Assertion(
            atype=AssertionType.EQUAL,
            setup_commands=['echo "hello world" > file.txt'],
            actual='cat file.txt',
            expected='hello world',
            data=data,
            )
        second_assertion = Assertion(
            atype=AssertionType.EQUAL,
            actual='cat file.txt | wc -m',
            expected='11',
            data=data,
            )
        test = Test(pointer='important test', assertions=[first_assertion, second_assertion], data=data)
        test_suite_node = TestsSuite(
            tests=[test],
            setup_commands=['echo "hello world" > file.txt'],
            teardown_commands=['echo "finished test"'],
            data=data,
            )

        actual = THE_MODULE.Interpreter().interpret(test_suite_node)

        expected = (
            '#!/usr/bin/env bats\n'
            '#\n'
            '# This test file was generated using Batspp\n'
            '# https://github.com/LimaBD/batspp\n'
            '#\n'
            '\n'
            '# Constants\n'
            'VERBOSE_DEBUG=""\n'
            'TEMP_DIR="/tmp"\n'
            '\n'
            '# Setup function\n'
            '# $1 -> test name\n'
            'function run_setup () {\n'
            '\ttest_folder=$(echo $TEMP_DIR/$1-$$)\n'
            '\tmkdir --parents "$test_folder"\n'
            '\tcd "$test_folder" || echo Warning: Unable to "cd $test_folder"\n'
            '\techo "hello world" > file.txt\n'
            '}\n'
            '\n'
            '# Teardown function\n'
            'function run_teardown () {\n'
            '\techo "finished test"\n'
            '}\n'
            '\n'
            '@test "important test" {\n'
            '\trun_setup "important-test"\n'
            '\n'
            '\t# Assertion of line 3\n'
            '\techo "hello world" > file.txt\n'
            '\tprint_debug "$(important-test-line3-actual)" "$(important-test-line3-expected)"\n'
            '\t[ "$(important-test-line3-actual)" == "$(important-test-line3-expected)" ]\n'
            '\n'
            '\t# Assertion of line 3\n'
            '\tprint_debug "$(important-test-line3-actual)" "$(important-test-line3-expected)"\n'
            '\t[ "$(important-test-line3-actual)" == "$(important-test-line3-expected)" ]\n'
            '\n'
            '\trun_teardown\n'
            '}\n'
            '\n'
            'function important-test-line3-actual () {\n'
            '\tcat file.txt\n'
            '}\n'
            '\n'
            'function important-test-line3-expected () {\n'
            '\techo -e \'hello world\'\n'
            '}\n'
            '\n'
            'function important-test-line3-actual () {\n'
            '\tcat file.txt | wc -m\n'
            '}\n'
            '\n'
            'function important-test-line3-expected () {\n'
            '\techo -e \'11\'\n'
            '}\n'
            '\n'
            '# This prints debug data when an assertion fail\n'
            '# $1 -> actual value\n'
            '# $2 -> expected value\n'
            'function print_debug() {\n'
            '\techo "=======  actual  ======="\n'
            '\tbash -c "echo \\"$1\\" $VERBOSE_DEBUG"\n'
            '\techo "======= expected ======="\n'
            '\tbash -c "echo \\"$2\\" $VERBOSE_DEBUG"\n'
            '\techo "========================"\n'
            '}\n'
            '\n'
            )

        assert actual == expected


if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
