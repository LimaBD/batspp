#!/usr/bin/env python3
#
# Tests for lexer.py module
#


"""Tests for lexer.py module"""


# Standard packages
import sys
import unittest


# Installed packages
from mezcla.unittest_wrapper import TestWrapper
from mezcla import debug


# Module being tested
#
# to avoid import errors, must install package with '$ pip install .'
sys.path.insert(0, './../batspp')
from lexer import TextLiner, Lexer, Token, TokenType


class TestTextLiner(TestWrapper):
    """Class for testcase definition"""
    script_module = TestWrapper.derive_tested_module_name(__file__)
    maxDiff       = None

    def test_is_column_safe(self):
        """Test for is_column_safe()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_is_column_safe(); self={self}")

        text = TextLiner('some text line')
        text.column = 3
        self.assertTrue(text.is_column_safe())
        text.column = 13
        self.assertTrue(text.is_column_safe())
        text.column = 14
        self.assertFalse(text.is_column_safe())
        text.column = 49
        self.assertFalse(text.is_column_safe())

    def test_is_line_safe(self):
        """Test for is_line_safe()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_is_line_safe(); self={self}")

        text = TextLiner('some text\nwith\nmultiple\nlines')
        self.assertEqual(text.lines, ['some text', 'with', 'multiple', 'lines'])
        self.assertTrue(text.is_line_safe())
        text.line = 3
        self.assertTrue(text.is_line_safe())
        text.line = 4
        self.assertFalse(text.is_line_safe())
        text.line = 40
        self.assertFalse(text.is_line_safe())

    def test_get_rest_line(self):
        """Test for get_rest_line()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_get_rest_line(); self={self}")

        text = TextLiner('this is an line to do tests')
        text.column = 0
        self.assertEqual(text.get_rest_line(), 'this is an line to do tests')
        text.column = 13
        self.assertEqual(text.get_rest_line(), 'ne to do tests')
        text.column = 23
        self.assertEqual(text.get_rest_line(), 'ests')
        text.column = 26
        self.assertEqual(text.get_rest_line(), 's')
        text.column = 27
        self.assertEqual(text.get_rest_line(), None)
        text.column = 123
        self.assertEqual(text.get_rest_line(), None)

    def test_get_current_line(self):
        """Test for get_current_line()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_get_current_line(); self={self}")

        text = TextLiner('some text\nwith\nmultiple\nlines')
        text.line = 0
        self.assertEqual(text.get_current_line(), 'some text')
        text.line = 2
        self.assertEqual(text.get_current_line(), 'multiple')
        text.line = 6
        self.assertEqual(text.get_current_line(), None)

    def test_advance_column(self):
        """Test for advance_column()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_advance_column(); self={self}")

        text = TextLiner('some text')
        self.assertEqual(text.column, 0)

        # Advance normal
        text.advance_column()
        self.assertEqual(text.column, 1)

        # Check arg
        text.advance_column(2)
        self.assertEqual(text.column, 3)

        # Check limit
        self.assertEqual(text.line, 0)
        text.advance_column(50)
        self.assertEqual(text.column, 0)
        self.assertEqual(text.line, 1)

    def test_advance_line(self):
        """Test for advance_line()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_advance_line(); self={self}")

        text = TextLiner('some text\nwith\nmultiple\nlines')
        self.assertEqual(text.line, 0)
        text.column = 3
        text.advance_line()
        self.assertEqual(text.column, 0)
        self.assertEqual(text.line, 1)
        text.advance_line()
        self.assertEqual(text.line, 2)


class TestLexer(TestWrapper):
    """Class for testcase definition"""
    script_module = TestWrapper.derive_tested_module_name(__file__)
    maxDiff       = None

    def tokenize(self, string: str, embedded_tests:bool = False) -> list:
        """
        Tokenize STRING, verify tokens and returned types
        """

        tokens = Lexer().tokenize(string, embedded_tests=embedded_tests)
        self.assertTrue(tokens)
        self.assertTrue(isinstance(tokens, list))

        for token in tokens:
            self.assertTrue(isinstance(token, Token))

        self.assertEqual(tokens[-1].type, TokenType.EOF)

        return tokens

    def assert_token(self,
                     expected_type: TokenType,
                     valids:list = None,
                     invalids:list = None) -> None:
        """
        Assert token type, the VALIDS and INVALIDS cases
        must be very insolated tests cases, only check for the
        first token
        """
        if valids:
            for valid in valids:
                tokens = self.tokenize(valid)
                self.assertEqual(tokens[0].type, expected_type)
        if invalids:
            for invalid in invalids:
                tokens = self.tokenize(invalid)
                self.assertNotEqual(tokens[0].type, expected_type)

    def tokenize_types(self, string:str, embedded_tests:bool = False) -> list:
        """Tokenize STRING and map by types"""

        tokens = self.tokenize(string, embedded_tests=embedded_tests)

        types = []
        for token in tokens:
            types.append(token.type)

        return types

    def test_minor(self):
        """Test for MINOR token type"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_minor(); self={self}")

        tokens = self.tokenize('\n')
        self.assertEqual(len(tokens), 2) # two tokens: MINOR and EOF
        self.assertEqual(tokens[0].type, TokenType.MINOR)

        # N minor lines should be treat as one minor token
        tokens = self.tokenize('\n\n\n\n\n')
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.MINOR)

    def test_peso(self):
        """Test for PESO token type"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_peso(); self={self}")

        valids = ['$', '$ some text']
        invalids = ['foo $ some text']
        self.assert_token(TokenType.PESO, valids=valids, invalids=invalids)

    def test_test(self):
        """Test for TEST token type"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_test(); self={self}")

        valids = ['# Test foobar', '# test foobar']
        invalids = ['# foobar foobar Test foobar',
                    '# foobar Test']
        self.assert_token(TokenType.TEST, valids=valids, invalids=invalids)

    def test_setup(self):
        """Test for SETUP token type"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_setup(); self={self}")

        valids = ['# Setup', '# setup of foobar']
        invalids = ['# foobar foobar Setup foobar',
                    '# foobar Setup']
        self.assert_token(TokenType.SETUP, valids=valids, invalids=invalids)

    def test_teardown(self):
        """Test for TEARDOWN token type"""
        ## TODO: WORK-IN-PROGRESS

    def test_continuation(self):
        """Test for CONTINUATION token type"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_continuation(); self={self}")

        valids = ['# Continuation of foobar',
                  '# continuation of foobar',
                  '# Continue of foobar']
        invalids = ['# foobar foobar Continuation foobar',
                    '# foobar continuation']
        self.assert_token(TokenType.CONTINUATION, valids=valids, invalids=invalids)

    def test_pointer(self):
        """Test for POINTER token type"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_pointer(); self={self}")

        types = self.tokenize_types('# Continuation of foobar')
        self.assertEqual(types[:2], [TokenType.CONTINUATION, TokenType.POINTER])
        self.assert_token(TokenType.POINTER, invalids=['# of foobar'])

    def test_assert_eq(self):
        """Test for ASSERT_EQ token type"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_assert_eq(); self={self}")

        types = self.tokenize_types('somefunction arg1 arg2 => expected result')
        self.assertEqual(types, [TokenType.TEXT,
                                 TokenType.ASSERT_EQ,
                                 TokenType.TEXT,
                                 TokenType.EOF])

    def test_assert_ne(self):
        """Test for ASSERT_NE token type"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_assert_ne(); self={self}")

        types = self.tokenize_types('somefunction arg1 arg2 =/> not expected result')
        self.assertEqual(types, [TokenType.TEXT,
                                 TokenType.ASSERT_NE,
                                 TokenType.TEXT,
                                 TokenType.EOF])

    def test_end_eof_tags(self):
        """Test for END and EOF tags"""
        types = self.tokenize_types('$ some command\nexpected text\n<EOF>\n<END>')
        self.assertEqual(types, [TokenType.PESO,
                                 TokenType.TEXT,
                                 TokenType.TEXT,
                                 TokenType.MINOR,
                                 TokenType.MINOR,
                                 TokenType.EOF])

    def test_blank(self):
        """Test for BLANK tag"""
        types = self.tokenize_types('$ some command\nexpected text\n<BLANK>\nwith an blank line')
        self.assertEqual(types, [TokenType.PESO,
                                 TokenType.TEXT,
                                 TokenType.TEXT,
                                 TokenType.TEXT,
                                 TokenType.TEXT,
                                 TokenType.EOF])

    def test_text(self):
        """Test for TEXT token type"""
        ## TODO: WORK-IN-PROGRESS

    def test_comments(self):
        """Test skip comments"""
        ## TODO: WORK-IN-PROGRESS


if __name__ == '__main__':
    unittest.main()
