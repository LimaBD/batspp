#!/usr/bin/env python3
#
# Tests for interpreter.py module
#


"""Tests for interpreter.py module"""


# Standard packages
import sys
import unittest


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import debug


# Local modules
sys.path.insert(0, './batspp')
from lexer import TokenData # type: ignore
from parser import ( # type: ignore
    Setup, AssertionType, Assertion, Test, TestsSuite
)
from interpreter import NodeVisitor, Interpreter # type: ignore


class TestNodeVisitor(TestWrapper):
    """Class for testcase definition"""
    script_module = None
    maxDiff       = None

    ## TODO: implement stub classes to test visitors

    def test_visit(self):
        """Test for visit()"""
        ## TODO: WORK-IN-PROGRESS

    def test_generic_visitor(self):
        """Test for generic_visitor()"""
        ## TODO: WORK-IN-PROGRESS


class TestInterpreter(TestWrapper):
    """Class for testcase definition"""
    script_module = None
    maxDiff       = None

    def test_visit_TestsSuite(self):
        """Test for visit_TestsSuite()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_visit_TestsSuite(); self={self}")
        ## TODO: WORK-IN-PROGRESS

    def test_visit_Setup(self):
        """Test for visit_Setup()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_visit_Setup(); self={self}")
        data = TokenData(text_line='some line', line=3, column=3)
        interpreter = Interpreter()

        # NOTE: the extra spaces on commands are used
        #       to ensure that commands are striped.

        # Global setup
        node = Setup(commands=['      echo "some line" > file.txt'], data=data)
        actual = interpreter.visit_Setup(node)
        self.assertEqual(actual, '# Setup\necho "some line" > file.txt\n\n')

        # Local setup
        interpreter.last_title = 'some test'
        commands = ['     echo "some line" > file.txt    ',
                    'echo "another line" >> file.txt     ']
        node = Setup(commands=commands, data=data)
        actual = interpreter.visit_Setup(node)
        self.assertEqual(actual, '\techo "some line" > file.txt\n\techo "another line" >> file.txt\n')

    def test_visit_Test(self):
        """Test for visit_Test()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_visit_Test(); self={self}")
        data = TokenData(text_line='some line', line=3, column=3)
        interpreter = Interpreter()

        interpreter.stack_functions = ['function some_function() ...',
                                       'function another_function() ...']
        node = Test(pointer='important test', assertions=[], data=data)
        actual = interpreter.visit_Test(node)

        self.assertEqual(interpreter.last_title, 'important test')
        self.assertTrue('@test "important test"' in actual)

        # Check functions
        self.assertFalse(interpreter.stack_functions)
        self.assertTrue('function some_function() ...' in actual)
        self.assertTrue('function another_function() ...' in actual)

    def test_visit_Assertion(self):
        """Test for visit_Assertion()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_visit_Assertion(); self={self}")
        data = TokenData(text_line='some line', line=3, column=3)
        interpreter = Interpreter()

        interpreter.last_title = 'important test'
        node = Assertion(atype=AssertionType.EQUAL,
                         actual='echo "some text"',
                         expected='some text',
                         data=data)
        actual = interpreter.visit_Assertion(node)

        self.assertEqual(len(interpreter.stack_functions), 2)
        self.assertTrue('echo "some text"' in interpreter.stack_functions[0])
        self.assertTrue('some text' in interpreter.stack_functions[1])

        actual_assertion = actual.splitlines()[-1]
        self.assertTrue(actual_assertion.startswith('\t[ '))
        self.assertTrue(' == ' in actual_assertion)
        self.assertTrue(actual_assertion.endswith(' ]'))

        self.assertTrue(interpreter.debug_required)

    def test_interpret(self):
        """Test for interpret()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestInterpreter.test_interpret(); self={self}")
        data = TokenData(text_line='some line', line=3, column=3)

        local_setup = Setup(commands=['echo "hello world" > file.txt'], data=data)
        first_assertion = Assertion(atype=AssertionType.EQUAL,
                                    setup=local_setup,
                                    actual='cat file.txt',
                                    expected='hello world',
                                    data=data)
        second_assertion = Assertion(atype=AssertionType.EQUAL,
                                    actual='cat file.txt | wc -m',
                                    expected='11',
                                    data=data)
        test = Test(pointer='important test', assertions=[first_assertion, second_assertion], data=data)
        global_setup = Setup(commands=['echo "hello world" > file.txt'])
        test_suite_node = TestsSuite(setup=global_setup,
                                     tests=[test],
                                     data=data)

        actual = Interpreter().interpret(test_suite_node)

        expected = ('#!/usr/bin/env bats\n'
                    '#\n'
                    '# This test file was generated using Batspp\n'
                    '# https://github.com/LimaBD/batspp\n'
                    '#\n'
                    '\n'
                    '# Constants\n'
                    'VERBOSE_DEBUG=""\n'
                    'TEMP_DIR="/tmp"\n'
                    '\n'
                    '# Setup\n'
                    'echo "hello world" > file.txt\n'
                    '\n'
                    '@test "important test" {\n'
                    '\ttest_folder=$(echo $TEMP_DIR/important-test-$$)\n'
                    '\tmkdir --parents "$test_folder"\n'
                    '\tcd "$test_folder" || echo Warning: Unable to "cd $test_folder"\n'
                    '\n'
                    '\t# Assertion of line 3\n'
                    '\techo "hello world" > file.txt\n'
                    '\tprint_debug "$(important-test-line3-actual)" "$(important-test-line3-expected)"\n'
                    '\t[ "$(important-test-line3-actual)" == "$(important-test-line3-expected)" ]\n'
                    '\n'
                    '\t# Assertion of line 3\n'
                    '\tprint_debug "$(important-test-line3-actual)" "$(important-test-line3-expected)"\n'
                    '\t[ "$(important-test-line3-actual)" == "$(important-test-line3-expected)" ]\n'
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
                    '\tbash -c "echo "$1" $VERBOSE_DEBUG"\n'
                    '\techo "======= expected ======="\n'
                    '\tbash -c "echo "$2" $VERBOSE_DEBUG"\n'
                    '\techo "========================"\n'
                    '}\n'
                    '\n')

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
