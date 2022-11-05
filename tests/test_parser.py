#!/usr/bin/env python3
#
# Tests for _parser module
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_parser.py
#


"""Tests for _parser module"""


# Standard packages
from sys import path as sys_path


# Installed packages
import pytest
from mezcla import debug


# Local packages
sys_path.insert(0, './batspp')
from batspp._token import Token, TokenVariant
from batspp._ast_nodes import (
    AssertionType, Assertion,
    TestsSuite, Test,
    )


# Reference to the module being tested
import batspp._parser as THE_MODULE


class TestParser:
    """Class for testcase definition"""

    def test_get_current_token(self):
        """Test for get_current_token()"""
        debug.trace(7, f'TestParser.test_get_current_token({self})')

        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.EOF, None),
            ]

        assert isinstance(parser.get_current_token(), Token)
        assert parser.get_current_token().variant == TokenVariant.PESO
        parser.index = 1
        assert parser.get_current_token().variant == TokenVariant.TEXT

    def test_peek_token(self):
        """Test for peek_token()"""
        debug.trace(7, f'TestParser.test_peek_token({self})')

        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.EOF, None),
            ]

        assert isinstance(parser.peek_token(), Token)
        assert parser.peek_token(1).variant == TokenVariant.TEXT
        assert parser.peek_token(2).variant == TokenVariant.EOF
        assert parser.peek_token(3) is None

    def test_eat(self):
        """Test for eat()"""
        debug.trace(7, f'TestParser.test_eat({self})')

        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.EOF, None),
            ]
        assert parser.index == 0
        parser.eat(TokenVariant.PESO)
        assert parser.index == 1
        parser.eat(TokenVariant.TEXT)
        assert parser.index == 2

        with pytest.raises(Exception):
            parser.eat(TokenVariant.TEXT)

    def test_is_command_next(self):
        """Test for is_command_next()"""
        debug.trace(7, f'TestParser.test_is_command_next({self})')
        parser = THE_MODULE.Parser()

        # Valid command pattern
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.EOF, None),
            ]
        assert parser.is_command_next()

        # Invalid command pattern
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEST, '# Test text'),
            Token(TokenVariant.EOF, None),
            ]
        assert not parser.is_command_next()

    def test_is_setup_command_next(self):
        """Test for is_setup_command_next()"""
        debug.trace(7, f'TestParser.test_is_setup_command_next({self})')
        parser = THE_MODULE.Parser()

        # Valid setup patern
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.EOF, None),
            ]
        assert parser.is_setup_command_next()

        # Multiple setup patterns
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.EOF, None),
            ]
        assert parser.is_setup_command_next()

        # Not a command pattern
        parser.tokens = [
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.EOF, None),
            ]
        assert not parser.is_setup_command_next()

        # Extra text token
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.TEXT, 'more text'),
            Token(TokenVariant.EOF, None),
            ]
        assert not parser.is_setup_command_next()

    def test_is_assertion_next(self):
        """Test for is_assertion_next()"""
        debug.trace(7, f'TestParser.test_is_assertion_next({self})')
        parser = THE_MODULE.Parser()

        # Valid assertion pattern
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.TEXT, 'more text'),
            Token(TokenVariant.EOF, None),
            ]
        assert parser.is_assertion_next()

        # Multiple setup pattern, should return false
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.EOF, None),
            ]
        assert not parser.is_assertion_next()

        # Valid assert eq patterns (assert ne should work same)
        parser.tokens = [
            Token(TokenVariant.TEXT, 'function arg1 arg2'),
            Token(TokenVariant.ASSERT_EQ, '=>'),
            Token(TokenVariant.TEXT, 'some expected text'),
            Token(TokenVariant.EOF, None),
            ]
        assert parser.is_assertion_next()

        # Invalid assert eq pattern
        parser.tokens = [
            Token(TokenVariant.TEXT, 'function arg1 arg2'),
            Token(TokenVariant.ASSERT_EQ, '=>'),
            Token(TokenVariant.EOF, None),
            ]
        assert not parser.is_assertion_next()

    def test_push_test_ast_node(self):
        """Test for push_test_ast_node"""
        debug.trace(7, f'TestParser.test_push_test_ast_node({self})')
        parser = THE_MODULE.Parser()

        # Check test pattern
        assert not parser.tests_ast_nodes_stack
        parser.tokens = [
            Token(TokenVariant.TEST, '# Test '),
            Token(TokenVariant.TEXT, 'some test title'),
            Token(TokenVariant.EOF, None),
            ]
        parser.push_test_ast_node()
        assert len(parser.tests_ast_nodes_stack) == 1
        assert parser.tests_ast_nodes_stack[0].reference == 'some test title'
        assert parser.tests_ast_nodes_stack[0].reference != 'wrong reference!'

        # A new test with reference
        parser.push_test_ast_node(reference='a new forced test')
        assert len(parser.tests_ast_nodes_stack) == 2
        assert parser.tests_ast_nodes_stack[1].reference == 'a new forced test'

    def test_break_continuation(self):
        """Test for break_continuation()"""
        debug.trace(7, f'TestParser.test_break_continuation({self})')
        parser = THE_MODULE.Parser()

        parser.tests_ast_nodes_stack.append(Test(reference='first test'))
        parser.tests_ast_nodes_stack.append(Test(reference='important test'))
        parser.tests_ast_nodes_stack.append(Test(reference='another test'))
        parser.tokens = [
            Token(TokenVariant.CONTINUATION, '# Continuation'),
            Token(TokenVariant.POINTER, ' of '),
            Token(TokenVariant.TEXT, 'important test'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some command'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.EOF, None),
            ]

        # Continuation pattern content should
        # be added to the test pointed
        assert not parser.tests_ast_nodes_stack[0].assertions
        assert not parser.tests_ast_nodes_stack[1].assertions
        assert not parser.tests_ast_nodes_stack[2].assertions
        parser.break_continuation()
        assert not parser.tests_ast_nodes_stack[0].assertions
        assert parser.tests_ast_nodes_stack[1].assertions
        assert not parser.tests_ast_nodes_stack[2].assertions
        # NOTE: about the assetion content, it
        # is the responsibility of another test

        # If continuation has empty reference, this should be setted to last test
        parser = THE_MODULE.Parser()
        parser.last_reference = 'important test'
        parser.tests_ast_nodes_stack = [Test(reference='important test', assertions=None)]
        parser.tokens = [
            Token(TokenVariant.CONTINUATION, '# Continuation'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some command'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.MINOR, ''),
            ]
        assert len(parser.tests_ast_nodes_stack[0].assertions) == 0
        parser.break_continuation()
        assert len(parser.tests_ast_nodes_stack[0].assertions) == 1

        ## TODO: test exception


    def test_break_setup_assertion(self):
        """Test for break_setup_assertion()"""
        debug.trace(7, f'TestParser.test_break_setup_assertion({self})')
        ## TODO: WORK-IN-PROGRESS

    def test_push_setup_commands(self):
        """Test for push_setup_commands()"""
        debug.trace(7, f'TestParser.test_push_setup_commands({self})')
        parser = THE_MODULE.Parser()

        # Global setup pattern
        assert not parser.setup_commands_stack
        parser.tokens = [
            Token(TokenVariant.SETUP, '# Setup'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some command'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'another command'),
            Token(TokenVariant.EOF, None),
            ]
        parser.push_setup_commands()
        assert len(parser.setup_commands_stack) == 1
        assert parser.setup_commands_stack[0][0] == ''
        assert parser.setup_commands_stack[0][0] != 'wrong reference!'

        # Check setup commands
        assert parser.setup_commands_stack[0][1] == ['some command', 'another command']
        assert parser.setup_commands_stack[0][1] != ['new wrong command']

        # Check for local setup pattern
        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenVariant.SETUP, '# Setup '),
            Token(TokenVariant.POINTER, ' of '),
            Token(TokenVariant.TEXT, 'important test'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some command'),
            Token(TokenVariant.EOF, None),
            ]
        parser.push_setup_commands()
        assert len(parser.setup_commands_stack) == 1
        assert parser.setup_commands_stack[0][0] == 'important test'
        assert parser.setup_commands_stack[0][0] != 'wrong reference!'

        # Check setup pattern without commands
        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some command'),
            Token(TokenVariant.EOF, None),
            ]
        assert not parser.setup_commands_stack
        parser.push_setup_commands(reference='some lonely setup')
        assert len(parser.setup_commands_stack) == 1
        assert parser.setup_commands_stack[0][0] == 'some lonely setup'

        # Check for setup without reference (should be setted to last test)
        parser = THE_MODULE.Parser()
        parser.last_reference = 'important test'
        parser.tokens = [
            Token(TokenVariant.SETUP, '# Setup'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some command'),
            Token(TokenVariant.EOF, None),
            ]
        parser.push_setup_commands()
        assert len(parser.setup_commands_stack) == 1
        assert parser.setup_commands_stack[0][0] == 'important test'

    def test_build_assertion(self):
        """Test for build_assertion()"""
        debug.trace(7, f'TestParser.test_build_assertion({self})')
        parser = THE_MODULE.Parser()

        parser.tests_ast_nodes_stack.append(Test(reference='first test'))
        parser.tests_ast_nodes_stack.append(Test(reference='important test'))
        parser.tests_ast_nodes_stack.append(Test(reference='another test'))
        parser.setup_commands_stack.append(('some test', []))
        parser.setup_commands_stack.append(('important test', ['some command']))
        parser.setup_commands_stack.append(('another test', []))
        parser.tokens = [
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some command'),
            Token(TokenVariant.TEXT, 'some text'),
            Token(TokenVariant.EOF, None),
            ]

        # Check that the assertion is added to the corresponding test
        assert len(parser.tests_ast_nodes_stack[0].assertions) == 0
        assert len(parser.tests_ast_nodes_stack[1].assertions) == 0
        assert len(parser.tests_ast_nodes_stack[2].assertions) == 0
        parser.build_assertion(reference='important test')
        assert len(parser.tests_ast_nodes_stack[0].assertions) == 0
        assert len(parser.tests_ast_nodes_stack[1].assertions) == 1
        assert len(parser.tests_ast_nodes_stack[2].assertions) == 0

        # Check actual and expected values
        assert parser.tests_ast_nodes_stack[1].assertions[0].actual == ['some command']
        assert parser.tests_ast_nodes_stack[1].assertions[0].expected == ['some text']
        assert parser.tests_ast_nodes_stack[1].assertions[0].expected != ['wrong text!']

        # Check setup stack and assertion
        assert len(parser.setup_commands_stack) == 2
        assert parser.setup_commands_stack[0][0] == 'some test'
        assert parser.setup_commands_stack[1][0] == 'another test'
        assert parser.tests_ast_nodes_stack[1].assertions[0].setup_commands[0] == 'some command'

        # Check for assertion eq
        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenVariant.TEXT, 'function arg1 arg2'),
            Token(TokenVariant.ASSERT_NE, ' =/> '),
            Token(TokenVariant.TEXT, 'not expected text'),
            Token(TokenVariant.EOF, None),
            ]
        parser.tests_ast_nodes_stack.append(Test(reference='important test'))
        parser.build_assertion(reference='important test')
        assertion = parser.tests_ast_nodes_stack[0].assertions[0]
        assert assertion.atype == AssertionType.NOT_EQUAL
        assert assertion.actual == ['function arg1 arg2']
        assert assertion.expected == ['not expected text']

    def test_pop_setup_commands(self):
        """Test for pop_setup()"""
        debug.trace(7, f'TestParser.test_pop_setup_commands({self})')
        parser = THE_MODULE.Parser()

        parser.setup_commands_stack = [
            ('some test', ['some command']),
            ('important test', ['some important command']),
            ('another test', ['some command']),
            ('important test', ['another important command']),
            ]
        result = parser.pop_setup_commands(reference='important test')

        assert isinstance(result, list)
        assert result == ['some important command', 'another important command']
        assert len(parser.setup_commands_stack) == 2

    def test_build_tests_suite(self):
        """Test for build_tests_suite()"""
        debug.trace(7, f'TestParser.test_build_tests_suite({self})')
        ## TODO: WORK-IN-PROGRESS

    def test_parse(self):
        """Test for parse()"""
        debug.trace(7, f'TestParser.test_parse({self})')
        parser = THE_MODULE.Parser()

        # Normal parser usage test
        tokens = [
            Token(TokenVariant.SETUP, ''),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some global command'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'another global command'),
            Token(TokenVariant.MINOR, ''),
            Token(TokenVariant.TEST, '# Test '),
            Token(TokenVariant.TEXT, 'testing parser'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'local setup command'),
            Token(TokenVariant.PESO, '$'),
            Token(TokenVariant.TEXT, 'some assertion command'),
            Token(TokenVariant.TEXT, 'expected text line 1'),
            Token(TokenVariant.TEXT, 'expected text line 2'),
            Token(TokenVariant.TEXT, 'expected text line 3'),
            Token(TokenVariant.MINOR, ''),
            Token(TokenVariant.EOF, None),
            ]
        tree = parser.parse(tokens)
        assert isinstance(tree, TestsSuite)
        # Check setup
        assert tree.setup_commands == ['some global command', 'another global command']
        assert tree.setup_commands != ['wrong command!']
        # Check tests
        assert len(tree.tests) == 1
        assert tree.tests[0].assertions[0].setup_commands == ['local setup command']
        assert tree.tests[0].assertions[0].actual == ['some assertion command']
        assert tree.tests[0].assertions[0].expected == ['expected text line 1', 'expected text line 2', 'expected text line 3']

        # Test when tokens list is empty
        with pytest.raises(Exception):
            parser.parse([])

        # Test when tokens list not finish with EOF
        with pytest.raises(Exception):
            parser.parse([
                Token(TokenVariant.TEXT, 'expected text line 2'),
                Token(TokenVariant.TEXT, 'expected text line 3'),
            ])


if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
