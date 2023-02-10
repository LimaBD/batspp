#!/usr/bin/env python3
#
# Tests for _lexer module
#
# This test must be runned with the command:
# $ PYTHONPATH="$(pwd):$PYTHONPATH" ./tests/test_lexer.py
#


"""Tests for _lexer module"""


# Standard packages
from sys import path as sys_path


# Installed packages
import pytest
from mezcla import debug


# Local packages
sys_path.insert(0, './batspp')
from batspp._token import (
    Token, TokenVariant,
    )


# Reference to the module being tested
import batspp._lexer as THE_MODULE


class TestTextLiner:
    """Class for testcase definition"""

    def test_is_column_safe(self):
        """Test for is_column_safe()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_is_column_safe(); self={self}")

        text = THE_MODULE.TextLiner('some text line')
        text.column = 3
        assert text.is_column_safe()
        text.column = 13
        assert text.is_column_safe()
        text.column = 14
        assert not text.is_column_safe()
        text.column = 49
        assert not text.is_column_safe()

    def test_is_line_safe(self):
        """Test for is_line_safe()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_is_line_safe(); self={self}")

        text = THE_MODULE.TextLiner('some text\nwith\nmultiple\nlines')
        assert text.lines == ['some text', 'with', 'multiple', 'lines']
        assert text.is_line_safe()
        text.line = 3
        assert text.is_line_safe()
        text.line = 4
        assert not text.is_line_safe()
        text.line = 40
        assert not text.is_line_safe()

    def test_get_rest_line(self):
        """Test for get_rest_line()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_get_rest_line(); self={self}")

        text = THE_MODULE.TextLiner('this is an line to do tests')
        text.column = 0
        assert text.get_rest_line() == 'this is an line to do tests'
        text.column = 13
        assert text.get_rest_line() == 'ne to do tests'
        text.column = 23
        assert text.get_rest_line() == 'ests'
        text.column = 26
        assert text.get_rest_line() == 's'
        text.column = 27
        assert text.get_rest_line() is None
        text.column = 123
        assert text.get_rest_line() is None

    def test_get_current_line(self):
        """Test for get_current_line()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_get_current_line(); self={self}")

        text = THE_MODULE.TextLiner('some text\nwith\nmultiple\nlines')
        text.line = 0
        assert text.get_current_line() == 'some text'
        text.line = 2
        assert text.get_current_line() == 'multiple'
        text.line = 6
        assert text.get_current_line() is None

    def test_advance_column(self):
        """Test for advance_column()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_advance_column(); self={self}")

        text = THE_MODULE.TextLiner('some text')
        assert text.column == 0

        # Advance normal
        text.advance_column()
        assert text.column == 1

        # Check arg
        text.advance_column(2)
        assert text.column == 3

        # Check limit
        assert text.line == 0
        text.advance_column(50)
        assert text.column == 0
        assert text.line == 1

    def test_advance_line(self):
        """Test for advance_line()"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestTextLiner.test_advance_line(); self={self}")

        text = THE_MODULE.TextLiner('some text\nwith\nmultiple\nlines')
        assert text.line == 0
        text.column = 3
        text.advance_line()
        assert text.column == 0
        assert text.line == 1
        text.advance_line()
        assert text.line == 2


class TestLexer:
    """Class for testcase definition"""
    script_module = None
    maxDiff       = None

    def tokenize(self, string: str, embedded_tests:bool = False) -> list:
        """
        Tokenize STRING, verify tokens and returned variants
        """

        tokens = THE_MODULE.Lexer().tokenize(string, embedded_tests=embedded_tests)
        assert tokens
        assert isinstance(tokens, list)

        for token in tokens:
            assert isinstance(token, Token)

        assert tokens[-1].variant == TokenVariant.EOF

        return tokens

    def assert_token(self,
                     expected_variant: TokenVariant,
                     valids:list = None,
                     invalids:list = None) -> None:
        """
        Assert token variant, the VALIDS and INVALIDS cases
        must be very insolated tests cases, only check for the
        first token
        """
        if valids:
            for valid in valids:
                tokens = self.tokenize(valid)
                assert tokens[0].variant == expected_variant
        if invalids:
            for invalid in invalids:
                tokens = self.tokenize(invalid)
                assert tokens[0].variant != expected_variant

    def tokenize_variants(self, string:str, embedded_tests:bool = False) -> list:
        """Tokenize STRING and map by variants"""
        tokens = self.tokenize(string, embedded_tests=embedded_tests)
        variants = [token.variant for token in tokens]
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.tokenize_variants() => {variants}")
        return variants

    def test_minor(self):
        """Test for MINOR token variant"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_minor(); self={self}")
        ## TODO: WORK-IN-PROGRESS

    def test_new_line(self):
        """Test for NEW_LINE token variant"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_new_line(); self={self}")
        tokens = self.tokenize('\n')
        assert len(tokens) == 2 # two tokens: MINOR and EOF
        assert tokens[0].variant == TokenVariant.NEW_LINE

    def test_peso(self):
        """Test for PESO token variant"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_peso(); self={self}")
        valids = [
            '$ some text',
            ]
        invalids = [
            'foo $ some text',
            ]
        self.assert_token(TokenVariant.PESO, valids=valids, invalids=invalids)

    def test_test(self):
        """Test for TEST token variant"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_test(); self={self}")
        valids = [
            '# Test foobar',
            '# test foobar',
            ]
        invalids = [
            '# foobar foobar Test foobar',
            '# foobar Test',
            ]
        self.assert_token(TokenVariant.TEST, valids=valids, invalids=invalids)

    def test_setup(self):
        """Test for SETUP token variant"""
        debug.trace(
            debug.QUITE_DETAILED,
            f"TestLexer.test_setup(); self={self}"
            )
        valids = [
            '# Setup',
            '# setup of foobar',
            ]
        invalids = [
            '# foobar foobar Setup foobar',
            '# foobar Setup',
            ]
        self.assert_token(TokenVariant.SETUP, valids=valids, invalids=invalids)

    def test_teardown(self):
        """Test for TEARDOWN token variant"""
        ## TODO: WORK-IN-PROGRESS

    def test_continuation(self):
        """Test for CONTINUATION token variant"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_continuation(); self={self}")
        valids = [
            '# Continuation of foobar',
            '# continuation of foobar',
            '# Continue of foobar',
            ]
        invalids = [
            '# foobar foobar Continuation foobar',
            '# foobar continuation',
            ]
        self.assert_token(TokenVariant.CONTINUATION, valids=valids, invalids=invalids)

    def test_pointer(self):
        """Test for POINTER token variant"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_pointer(); self={self}")

        variants = self.tokenize_variants('# Continuation of foobar')
        assert variants[:2] == [TokenVariant.CONTINUATION, TokenVariant.POINTER]
        self.assert_token(TokenVariant.POINTER, invalids=['# of foobar'])

    def test_assert_eq(self):
        """Test for ASSERT_EQ token variant"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_assert_eq(); self={self}")

        variants = self.tokenize_variants('somefunction arg1 arg2 => expected result')
        assert variants == [
            TokenVariant.TEXT,
            TokenVariant.ASSERT_EQ,
            TokenVariant.TEXT,
            TokenVariant.EOF,
            ]

    def test_assert_ne(self):
        """Test for ASSERT_NE token variant"""
        debug.trace(debug.QUITE_DETAILED,
                    f"TestLexer.test_assert_ne(); self={self}")

        variants = self.tokenize_variants('somefunction arg1 arg2 =/> not expected result')
        assert variants == [
            TokenVariant.TEXT,
            TokenVariant.ASSERT_NE,
            TokenVariant.TEXT,
            TokenVariant.EOF,
            ]

    def test_end_eof_tags(self):
        """Test for END and EOF tags"""
        variants = self.tokenize_variants('$ some command\nexpected text\n<EOF>\n<END>')
        assert variants == [
            TokenVariant.PESO,
            TokenVariant.TEXT,
            TokenVariant.TEXT,
            TokenVariant.MINOR,
            TokenVariant.MINOR,
            TokenVariant.EOF,
            ]

    def test_blank(self):
        """Test for BLANK tag"""
        variants = self.tokenize_variants('$ some command\nexpected text\n<BLANK>\nwith an blank line')
        assert variants == [
            TokenVariant.PESO,
            TokenVariant.TEXT,
            TokenVariant.TEXT,
            TokenVariant.TEXT,
            TokenVariant.TEXT,
            TokenVariant.EOF,
            ]

    def test_text(self):
        """Test for TEXT token variant"""
        ## TODO: WORK-IN-PROGRESS

    def test_comments(self):
        """Test skip comments"""
        ## TODO: WORK-IN-PROGRESS


if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
