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
from batspp._token import Token, TokenType
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
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None),
            ]

        assert isinstance(parser.get_current_token(), Token)
        assert parser.get_current_token().type == TokenType.PESO
        parser.index = 1
        assert parser.get_current_token().type == TokenType.TEXT

    def test_peek_token(self):
        """Test for peek_token()"""
        debug.trace(7, f'TestParser.test_peek_token({self})')

        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None),
            ]

        assert isinstance(parser.peek_token(), Token)
        assert parser.peek_token(1).type == TokenType.TEXT
        assert parser.peek_token(2).type == TokenType.EOF
        assert parser.peek_token(3) == None

    def test_eat(self):
        """Test for eat()"""
        debug.trace(7, f'TestParser.test_eat({self})')

        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None),
            ]
        assert parser.index == 0
        parser.eat(TokenType.PESO)
        assert parser.index == 1
        parser.eat(TokenType.TEXT)
        assert parser.index == 2

        with pytest.raises(Exception):
            parser.eat(TokenType.TEXT)

    def test_is_command_next(self):
        """Test for is_command_next()"""
        debug.trace(7, f'TestParser.test_is_command_next({self})')
        parser = THE_MODULE.Parser()

        # Valid command pattern
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None),
            ]
        assert parser.is_command_next()

        # Invalid command pattern
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEST, '# Test text'),
            Token(TokenType.EOF, None),
            ]
        assert not parser.is_command_next()

    def test_is_setup_command_next(self):
        """Test for is_setup_command_next()"""
        debug.trace(7, f'TestParser.test_is_setup_command_next({self})')
        parser = THE_MODULE.Parser()

        # Valid setup patern
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None),
            ]
        assert parser.is_setup_command_next()

        # Multiple setup patterns
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None),
            ]
        assert parser.is_setup_command_next()

        # Not a command pattern
        parser.tokens = [
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None),
            ]
        assert not parser.is_setup_command_next()

        # Extra text token
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.TEXT, 'more text'),
            Token(TokenType.EOF, None),
            ]
        assert not parser.is_setup_command_next()

    def test_is_assertion_next(self):
        """Test for is_assertion_next()"""
        debug.trace(7, f'TestParser.test_is_assertion_next({self})')
        parser = THE_MODULE.Parser()

        # Valid assertion pattern
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.TEXT, 'more text'),
            Token(TokenType.EOF, None),
            ]
        assert parser.is_assertion_next()

        # Multiple setup pattern, should return false
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None),
            ]
        assert not parser.is_assertion_next()

        # Valid assert eq patterns (assert ne should work same)
        parser.tokens = [
            Token(TokenType.TEXT, 'function arg1 arg2'),
            Token(TokenType.ASSERT_EQ, '=>'),
            Token(TokenType.TEXT, 'some expected text'),
            Token(TokenType.EOF, None),
            ]
        assert parser.is_assertion_next()

        # Invalid assert eq pattern
        parser.tokens = [
            Token(TokenType.TEXT, 'function arg1 arg2'),
            Token(TokenType.ASSERT_EQ, '=>'),
            Token(TokenType.EOF, None),
            ]
        assert not parser.is_assertion_next()

    def test_build_test(self):
        """Test for build_test()"""
        debug.trace(7, f'TestParser.test_build_test({self})')
        parser = THE_MODULE.Parser()

        # Check test pattern
        assert not parser.test_nodes
        parser.tokens = [
            Token(TokenType.TEST, '# Test '),
            Token(TokenType.TEXT, 'some test title'),
            Token(TokenType.EOF, None),
            ]
        parser.build_test()
        assert len(parser.test_nodes) == 1
        assert parser.test_nodes[0].pointer == 'some test title'
        assert parser.test_nodes[0].pointer != 'wrong pointer!'

        # A new test with pointer
        parser.build_test(pointer='a new forced test')
        assert len(parser.test_nodes) == 2
        assert parser.test_nodes[1].pointer == 'a new forced test'

    def test_break_continuation(self):
        """Test for break_continuation()"""
        debug.trace(7, f'TestParser.test_break_continuation({self})')
        parser = THE_MODULE.Parser()

        parser.test_nodes.append(Test(pointer='first test'))
        parser.test_nodes.append(Test(pointer='important test'))
        parser.test_nodes.append(Test(pointer='another test'))
        parser.tokens = [
            Token(TokenType.CONTINUATION, '# Continuation'),
            Token(TokenType.POINTER, ' of '),
            Token(TokenType.TEXT, 'important test'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None),
            ]

        # Continuation pattern content should
        # be added to the test pointed
        assert not parser.test_nodes[0].assertions
        assert not parser.test_nodes[1].assertions
        assert not parser.test_nodes[2].assertions
        parser.break_continuation()
        assert not parser.test_nodes[0].assertions
        assert parser.test_nodes[1].assertions
        assert not parser.test_nodes[2].assertions
        # NOTE: about the assetion content, it
        # is the responsibility of another test

        # If continuation has empty pointer, this should be setted to last test
        parser = THE_MODULE.Parser()
        parser.last_pointer = 'important test'
        parser.test_nodes = [Test(pointer='important test', assertions=None)]
        parser.tokens = [
            Token(TokenType.CONTINUATION, '# Continuation'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.MINOR, ''),
            ]
        assert len(parser.test_nodes[0].assertions) == 0
        parser.break_continuation()
        assert len(parser.test_nodes[0].assertions) == 1

        ## TODO: test exception


    def test_break_setup_assertion(self):
        """Test for break_setup_assertion()"""
        debug.trace(7, f'TestParser.test_break_setup_assertion({self})')
        ## TODO: WORK-IN-PROGRESS

    def test_append_setup_commands(self):
        """Test for append_setup_commands()"""
        debug.trace(7, f'TestParser.test_append_setup_commands({self})')
        parser = THE_MODULE.Parser()

        # Global setup pattern
        assert not parser.setup_commands_stack
        parser.tokens = [
            Token(TokenType.SETUP, '# Setup'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'another command'),
            Token(TokenType.EOF, None),
            ]
        parser.append_setup_commands()
        assert len(parser.setup_commands_stack) == 1
        assert parser.setup_commands_stack[0][0] == ''
        assert parser.setup_commands_stack[0][0] != 'wrong pointer!'

        # Check setup commands
        assert parser.setup_commands_stack[0][1] == ['some command', 'another command']
        assert parser.setup_commands_stack[0][1] != ['new wrong command']

        # Check for local setup pattern
        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenType.SETUP, '# Setup '),
            Token(TokenType.POINTER, ' of '),
            Token(TokenType.TEXT, 'important test'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.EOF, None),
            ]
        parser.append_setup_commands()
        assert len(parser.setup_commands_stack) == 1
        assert parser.setup_commands_stack[0][0] == 'important test'
        assert parser.setup_commands_stack[0][0] != 'wrong pointer!'

        # Check setup pattern without commands
        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.EOF, None),
            ]
        assert not parser.setup_commands_stack
        parser.append_setup_commands(pointer='some lonely setup')
        assert len(parser.setup_commands_stack) == 1
        assert parser.setup_commands_stack[0][0] == 'some lonely setup'

        # Check for setup without pointer (should be setted to last test)
        parser = THE_MODULE.Parser()
        parser.last_pointer = 'important test'
        parser.tokens = [
            Token(TokenType.SETUP, '# Setup'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.EOF, None),
            ]
        parser.append_setup_commands()
        assert len(parser.setup_commands_stack) == 1
        assert parser.setup_commands_stack[0][0] == 'important test'

    def test_build_assertion(self):
        """Test for build_assertion()"""
        debug.trace(7, f'TestParser.test_build_assertion({self})')
        parser = THE_MODULE.Parser()

        parser.test_nodes.append(Test(pointer='first test'))
        parser.test_nodes.append(Test(pointer='important test'))
        parser.test_nodes.append(Test(pointer='another test'))
        parser.setup_commands_stack.append(('some test', []))
        parser.setup_commands_stack.append(('important test', ['some command']))
        parser.setup_commands_stack.append(('another test', []))
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None),
            ]

        # Check that the assertion is added to the corresponding test
        assert len(parser.test_nodes[0].assertions) == 0
        assert len(parser.test_nodes[1].assertions) == 0
        assert len(parser.test_nodes[2].assertions) == 0
        parser.build_assertion(pointer='important test')
        assert len(parser.test_nodes[0].assertions) == 0
        assert len(parser.test_nodes[1].assertions) == 1
        assert len(parser.test_nodes[2].assertions) == 0

        # Check actual and expected values
        assert parser.test_nodes[1].assertions[0].actual == 'some command'
        assert parser.test_nodes[1].assertions[0].expected == 'some text'
        assert parser.test_nodes[1].assertions[0].expected != 'wrong text!'

        # Check setup stack and assertion
        assert len(parser.setup_commands_stack) == 2
        assert parser.setup_commands_stack[0][0] == 'some test'
        assert parser.setup_commands_stack[1][0] == 'another test'
        assert parser.test_nodes[1].assertions[0].setup_commands[0] == 'some command'

        # Check for assertion eq
        parser = THE_MODULE.Parser()
        parser.tokens = [
            Token(TokenType.TEXT, 'function arg1 arg2'),
            Token(TokenType.ASSERT_NE, ' =/> '),
            Token(TokenType.TEXT, 'not expected text'),
            Token(TokenType.EOF, None),
            ]
        parser.test_nodes.append(Test(pointer='important test'))
        parser.build_assertion(pointer='important test')
        assertion = parser.test_nodes[0].assertions[0]
        assert assertion.atype == AssertionType.NOT_EQUAL
        assert assertion.actual == 'function arg1 arg2'
        assert assertion.expected == 'not expected text'

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
        result = parser.pop_setup_commands(pointer='important test')

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
            Token(TokenType.SETUP, ''),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some global command'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'another global command'),
            Token(TokenType.MINOR, ''),
            Token(TokenType.TEST, '# Test '),
            Token(TokenType.TEXT, 'testing parser'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'local setup command'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some assertion command'),
            Token(TokenType.TEXT, 'expected text line 1'),
            Token(TokenType.TEXT, 'expected text line 2'),
            Token(TokenType.TEXT, 'expected text line 3'),
            Token(TokenType.MINOR, ''),
            Token(TokenType.EOF, None),
            ]
        tree = parser.parse(tokens)
        assert isinstance(tree, TestsSuite)\
        # Check setup
        assert tree.setup_commands == ['some global command', 'another global command']
        assert tree.setup_commands != ['wrong command!']
        # Check tests
        assert len(tree.tests) == 1
        assert tree.tests[0].assertions[0].setup_commands == ['local setup command']
        assert tree.tests[0].assertions[0].actual == 'some assertion command'
        assert tree.tests[0].assertions[0].expected == 'expected text line 1\nexpected text line 2\nexpected text line 3'

        # Test when tokens list is empty
        with pytest.raises(Exception):
            parser.parse([])

        # Test when tokens list not finish with EOF
        with pytest.raises(Exception):
            parser.parse([
                Token(TokenType.TEXT, 'expected text line 2'),
                Token(TokenType.TEXT, 'expected text line 3'),
            ])


if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
