#!/usr/bin/env python3
#
# Tests for parser.py module
#


"""Tests for parser.py module"""


# Standard packages
import sys
import unittest


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import debug


# Local modules
sys.path.insert(0, './batspp')
from _tokens import Token, TokenType # type: ignore
from _parser import Parser # type: ignore
from _ast_nodes import ( # type: ignore
    AssertionType, Assertion,
    TestsSuite, Test 
)


class TestParser(TestWrapper):
    """Class for testcase definition"""
    script_module = None
    maxDiff       = None

    def test_get_current_token(self):
        """Test for get_current_token()"""
        debug.trace(7, f'TestParser.test_get_current_token({self})')

        parser = Parser()
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None)
        ]

        self.assertTrue(isinstance(parser.get_current_token(), Token))
        self.assertEqual(parser.get_current_token().type, TokenType.PESO)
        parser.index = 1
        self.assertEqual(parser.get_current_token().type, TokenType.TEXT)

    def test_peek_token(self):
        """Test for peek_token()"""
        debug.trace(7, f'TestParser.test_peek_token({self})')

        parser = Parser()
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None)
        ]

        self.assertTrue(isinstance(parser.peek_token(), Token))
        self.assertEqual(parser.peek_token(1).type, TokenType.TEXT)
        self.assertEqual(parser.peek_token(2).type, TokenType.EOF)
        self.assertEqual(parser.peek_token(3), None)

    def test_eat(self):
        """Test for eat()"""
        debug.trace(7, f'TestParser.test_eat({self})')

        parser = Parser()
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None)
        ]
        self.assertEqual(parser.index, 0)
        parser.eat(TokenType.PESO)
        self.assertEqual(parser.index, 1)
        parser.eat(TokenType.TEXT)
        self.assertEqual(parser.index, 2)
        with self.assertRaises(Exception):
            parser.eat(TokenType.TEXT)

    def test_is_command_next(self):
        """Test for is_command_next()"""
        debug.trace(7, f'TestParser.test_is_command_next({self})')
        parser = Parser()

        # Valid command pattern
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None)
        ]
        self.assertTrue(parser.is_command_next())

        # Invalid command pattern
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEST, '# Test text'),
            Token(TokenType.EOF, None)
        ]
        self.assertFalse(parser.is_command_next())

    def test_is_pure_command_next(self):
        """Test for is_pure_command_next()"""
        debug.trace(7, f'TestParser.test_is_pure_command_next({self})')
        parser = Parser()

        # Valid setup patern
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None)
        ]
        self.assertTrue(parser.is_pure_command_next())

        # Multiple setup patterns
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None)
        ]
        self.assertTrue(parser.is_pure_command_next())

        # Not a command pattern
        parser.tokens = [
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None)
        ]
        self.assertFalse(parser.is_pure_command_next())

        # Extra text token
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.TEXT, 'more text'),
            Token(TokenType.EOF, None)
        ]
        self.assertFalse(parser.is_pure_command_next())

    def test_is_assertion_next(self):
        """Test for is_assertion_next()"""
        debug.trace(7, f'TestParser.test_is_assertion_next({self})')
        parser = Parser()

        # Valid assertion pattern
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.TEXT, 'more text'),
            Token(TokenType.EOF, None)
        ]
        self.assertTrue(parser.is_assertion_next())

        # Multiple setup pattern, should return false
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.EOF, None)
        ]
        self.assertFalse(parser.is_assertion_next())

        # Valid assert eq patterns (assert ne should work same)
        parser.tokens = [
            Token(TokenType.TEXT, 'function arg1 arg2'),
            Token(TokenType.ASSERT_EQ, '=>'),
            Token(TokenType.TEXT, 'some expected text'),
            Token(TokenType.EOF, None)
        ]
        self.assertTrue(parser.is_assertion_next())

        # Invalid assert eq pattern
        parser.tokens = [
            Token(TokenType.TEXT, 'function arg1 arg2'),
            Token(TokenType.ASSERT_EQ, '=>'),
            Token(TokenType.EOF, None)
        ]
        self.assertFalse(parser.is_assertion_next())

    def test_build_test(self):
        """Test for build_test()"""
        debug.trace(7, f'TestParser.test_build_test({self})')
        parser = Parser()

        # Check test pattern
        self.assertFalse(parser.test_nodes)
        parser.tokens = [
            Token(TokenType.TEST, '# Test '),
            Token(TokenType.TEXT, 'some test title'),
            Token(TokenType.EOF, None)
        ]
        parser.build_test()
        self.assertEqual(len(parser.test_nodes), 1)
        self.assertEqual(parser.test_nodes[0].pointer, 'some test title')
        self.assertNotEqual(parser.test_nodes[0].pointer, 'wrong pointer!')

        # A new test with pointer
        parser.build_test(pointer='a new forced test')
        self.assertEqual(len(parser.test_nodes), 2)
        self.assertEqual(parser.test_nodes[1].pointer, 'a new forced test')

    def test_break_continuation(self):
        """Test for break_continuation()"""
        debug.trace(7, f'TestParser.test_break_continuation({self})')
        parser = Parser()

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
            Token(TokenType.EOF, None)
        ]

        # Continuation pattern content should
        # be added to the test pointed
        self.assertFalse(parser.test_nodes[0].assertions)
        self.assertFalse(parser.test_nodes[1].assertions)
        self.assertFalse(parser.test_nodes[2].assertions)
        parser.break_continuation()
        self.assertFalse(parser.test_nodes[0].assertions)
        self.assertTrue(parser.test_nodes[1].assertions)
        self.assertFalse(parser.test_nodes[2].assertions)
        # NOTE: about the assetion content, it
        # is the responsibility of another test

        # If continuation has empty pointer, this should be setted to last test
        parser = Parser()
        parser.last_pointer = 'important test'
        parser.test_nodes = [Test(pointer='important test', assertions=None)]
        parser.tokens = [
            Token(TokenType.CONTINUATION, '# Continuation'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.TEXT, 'some text'),
            Token(TokenType.MINOR, '')
        ]
        self.assertEqual(len(parser.test_nodes[0].assertions), 0)
        parser.break_continuation()
        self.assertEqual(len(parser.test_nodes[0].assertions), 1)

        ## TODO: test exception


    def test_break_setup_assertion(self):
        """Test for break_setup_assertion()"""
        debug.trace(7, f'TestParser.test_break_setup_assertion({self})')
        ## TODO: WORK-IN-PROGRESS

    def test_append_setup_commands(self):
        """Test for append_setup_commands()"""
        debug.trace(7, f'TestParser.test_append_setup_commands({self})')
        parser = Parser()

        # Global setup pattern
        self.assertFalse(parser.setup_commands_stack)
        parser.tokens = [
            Token(TokenType.SETUP, '# Setup'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'another command'),
            Token(TokenType.EOF, None)
        ]
        parser.append_setup_commands()
        self.assertEqual(len(parser.setup_commands_stack), 1)
        self.assertEqual(parser.setup_commands_stack[0][0], '')
        self.assertNotEqual(parser.setup_commands_stack[0][0], 'wrong pointer!')

        # Check setup commands
        self.assertEqual(parser.setup_commands_stack[0][1], ['some command', 'another command'])
        self.assertNotEqual(parser.setup_commands_stack[0][1], ['new wrong command'])

        # Check for local setup pattern
        parser = Parser()
        parser.tokens = [
            Token(TokenType.SETUP, '# Setup '),
            Token(TokenType.POINTER, ' of '),
            Token(TokenType.TEXT, 'important test'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.EOF, None)
        ]
        parser.append_setup_commands()
        self.assertEqual(len(parser.setup_commands_stack), 1)
        self.assertEqual(parser.setup_commands_stack[0][0], 'important test')
        self.assertNotEqual(parser.setup_commands_stack[0][0], 'wrong pointer!')

        # Check setup pattern without commands
        parser = Parser()
        parser.tokens = [
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.EOF, None)
        ]
        self.assertFalse(parser.setup_commands_stack)
        parser.append_setup_commands(pointer='some lonely setup')
        self.assertEqual(len(parser.setup_commands_stack), 1)
        self.assertEqual(parser.setup_commands_stack[0][0], 'some lonely setup')

        # Check for setup without pointer (should be setted to last test)
        parser = Parser()
        parser.last_pointer = 'important test'
        parser.tokens = [
            Token(TokenType.SETUP, '# Setup'),
            Token(TokenType.PESO, '$'),
            Token(TokenType.TEXT, 'some command'),
            Token(TokenType.EOF, None)
        ]
        parser.append_setup_commands()
        self.assertEqual(len(parser.setup_commands_stack), 1)
        self.assertEqual(parser.setup_commands_stack[0][0], 'important test')

    def test_build_assertion(self):
        """Test for build_assertion()"""
        debug.trace(7, f'TestParser.test_build_assertion({self})')
        parser = Parser()

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
            Token(TokenType.EOF, None)
        ]

        # Check that the assertion is added to the corresponding test
        self.assertEqual(len(parser.test_nodes[0].assertions), 0)
        self.assertEqual(len(parser.test_nodes[1].assertions), 0)
        self.assertEqual(len(parser.test_nodes[2].assertions), 0)
        parser.build_assertion(pointer='important test')
        self.assertEqual(len(parser.test_nodes[0].assertions), 0)
        self.assertEqual(len(parser.test_nodes[1].assertions), 1)
        self.assertEqual(len(parser.test_nodes[2].assertions), 0)

        # Check actual and expected values
        self.assertEqual(parser.test_nodes[1].assertions[0].actual, 'some command')
        self.assertEqual(parser.test_nodes[1].assertions[0].expected, 'some text')
        self.assertNotEqual(parser.test_nodes[1].assertions[0].expected, 'wrong text!')

        # Check setup stack and assertion
        self.assertEqual(len(parser.setup_commands_stack), 2)
        self.assertEqual(parser.setup_commands_stack[0][0], 'some test')
        self.assertEqual(parser.setup_commands_stack[1][0], 'another test')
        self.assertEqual(parser.test_nodes[1].assertions[0].setup_commands[0], 'some command')

        # Check for assertion eq
        parser = Parser()
        parser.tokens = [
            Token(TokenType.TEXT, 'function arg1 arg2'),
            Token(TokenType.ASSERT_NE, ' =/> '),
            Token(TokenType.TEXT, 'not expected text'),
            Token(TokenType.EOF, None)
        ]
        parser.test_nodes.append(Test(pointer='important test'))
        parser.build_assertion(pointer='important test')
        assertion = parser.test_nodes[0].assertions[0]
        self.assertEqual(assertion.atype, AssertionType.NOT_EQUAL)
        self.assertEqual(assertion.actual, 'function arg1 arg2')
        self.assertEqual(assertion.expected, 'not expected text')

    def test_pop_setup_commands(self):
        """Test for pop_setup()"""
        debug.trace(7, f'TestParser.test_pop_setup_commands({self})')
        parser = Parser()

        parser.setup_commands_stack = [
            ('some test', ['some command']),
            ('important test', ['some important command']),
            ('another test', ['some command']),
            ('important test', ['another important command'])
        ]
        result = parser.pop_setup_commands(pointer='important test')

        self.assertTrue(isinstance(result, list))
        self.assertEqual(result, ['some important command', 'another important command'])
        self.assertEqual(len(parser.setup_commands_stack), 2)

    def test_build_tests_suite(self):
        """Test for build_tests_suite()"""
        debug.trace(7, f'TestParser.test_build_tests_suite({self})')
        ## TODO: WORK-IN-PROGRESS

    def test_parse(self):
        """Test for parse()"""
        debug.trace(7, f'TestParser.test_parse({self})')
        parser = Parser()

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
            Token(TokenType.EOF, None)
        ]
        tree = parser.parse(tokens)
        self.assertTrue(isinstance(tree, TestsSuite))

        # Check setup
        self.assertEqual(tree.setup_commands, ['some global command', 'another global command'])
        self.assertNotEqual(tree.setup_commands, ['wrong command!'])

        # Check tests
        self.assertEqual(len(tree.tests), 1)
        self.assertEqual(tree.tests[0].assertions[0].setup_commands, ['local setup command'])
        self.assertEqual(tree.tests[0].assertions[0].actual, 'some assertion command')
        self.assertEqual(tree.tests[0].assertions[0].expected, 'expected text line 1\nexpected text line 2\nexpected text line 3')

if __name__ == '__main__':
    unittest.main()
