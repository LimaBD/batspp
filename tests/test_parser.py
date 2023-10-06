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

# Reference to the module being tested
from batspp._parser import _Rule
from batspp._token import (
    Token, TokenData,
    )

# Tokens for testing purposes
TOKEN_ONE = 'TOKEN_ONE'
TOKEN_TWO = 'TOKEN_TWO'

# AST nodes for testing purposes
class TestAstNode():
    """AST node for testing purposes"""
    def __init__(self, *children) -> None:
        self.children = children

class TestRule:
    """Class for testcase definition"""

    def generate_token(self, variant:str):
        """Generate a token for testing purposes"""
        return Token(variant, 'some value', data=TokenData('', 1, 1))

    def generate_list_of_tokens(self, variants:list):
        """Generate a list of tokens for testing purposes"""
        return [self.generate_token(variant) for variant in variants]

    def assert_tokens_variants(self, tokens:list, variants:list):
        """Assert that the tokens variants are the expected"""
        # NOTE: not use zip(tokens, variants) because it stops at the shortest list
        for i, token in enumerate(tokens):
            variant = variants[i]
            if variant is None:
                assert token is None
            else:
                assert token.variant == variant

    def test_expect(self):
        """Test for expect() rule method"""
        rule = _Rule(TestAstNode, None) \
            .expect(TOKEN_ONE).expect(TOKEN_ONE) \
            .expect(TOKEN_TWO)
        # Happy case
        variants = [TOKEN_ONE, TOKEN_ONE, TOKEN_TWO]
        tokens = self.generate_list_of_tokens(variants)
        result, _ = rule.build_tree_from(tokens)
        self.assert_tokens_variants(result.children, variants)
        # Unhappy case
        with pytest.raises(SyntaxError) as exc_info:
            variants = [TOKEN_ONE, TOKEN_ONE, TOKEN_ONE]
            tokens = self.generate_list_of_tokens(variants)
            result, _ = rule.build_tree_from(tokens)
        assert 'Expected "TOKEN_TWO" but got "TOKEN_ONE"' in str(exc_info.value)

    def test_optionally(self):
        """Test for optionally() rule method"""
        rule = _Rule(TestAstNode, None) \
            .optionally(TOKEN_ONE).expect(TOKEN_TWO)
        # Happy case 1
        variants = [TOKEN_ONE, TOKEN_TWO]
        tokens = self.generate_list_of_tokens(variants)
        result, _ = rule.build_tree_from(tokens)
        self.assert_tokens_variants(result.children, variants)
        # Happy case 2
        tokens = self.generate_list_of_tokens([TOKEN_TWO])
        result, _ = rule.build_tree_from(tokens)
        self.assert_tokens_variants(result.children, [None, TOKEN_TWO])

    def test_zero_or_more(self):
        """Test for zero_or_more() rule method"""
        rule = _Rule(TestAstNode, None) \
            .zero_or_more(TOKEN_ONE)
        # Happy case 1
        variants = [TOKEN_ONE, TOKEN_ONE, TOKEN_ONE, TOKEN_ONE]
        tokens = self.generate_list_of_tokens(variants)
        result, _ = rule.build_tree_from(tokens)
        self.assert_tokens_variants(result.children[0], variants)
        # Happy case 2
        tokens = self.generate_list_of_tokens([TOKEN_ONE, TOKEN_ONE, TOKEN_TWO, TOKEN_TWO])
        result, _ = rule.build_tree_from(tokens)
        self.assert_tokens_variants(result.children[0], [TOKEN_ONE, TOKEN_ONE])

    def test_one_or_more(self):
        """Test for one_or_more() rule method"""
        rule = _Rule(TestAstNode, None) \
            .one_or_more(TOKEN_TWO)
        # Happy case 1
        variants = [TOKEN_TWO, TOKEN_TWO, TOKEN_TWO, TOKEN_TWO]
        tokens = self.generate_list_of_tokens(variants)
        result, _ = rule.build_tree_from(tokens)
        self.assert_tokens_variants(result.children[0], variants)
        # Unhappy case
        with pytest.raises(SyntaxError) as exc_info:
            variants = [TOKEN_ONE, TOKEN_TWO, TOKEN_TWO, TOKEN_TWO]
            tokens = self.generate_list_of_tokens(variants)
            result, _ = rule.build_tree_from(tokens)
        assert 'Expected "TOKEN_TWO" but got "TOKEN_ONE"' in str(exc_info.value)

    def test_ignore_next(self):
        """Test for ignore_next() rule method"""
        rule = _Rule(TestAstNode, None) \
            .ignore_next(TOKEN_ONE).expect(TOKEN_TWO)
        # Happy case 1
        variants = [TOKEN_ONE, TOKEN_ONE, TOKEN_TWO, TOKEN_ONE]
        tokens = self.generate_list_of_tokens(variants)
        result, _ = rule.build_tree_from(tokens)
        self.assert_tokens_variants(result.children, [TOKEN_TWO])
        # Happy case 2
        tokens = self.generate_list_of_tokens([TOKEN_TWO, TOKEN_ONE, TOKEN_ONE])
        result, _ = rule.build_tree_from(tokens)
        self.assert_tokens_variants(result.children, [TOKEN_TWO])

    def test_until(self):
        """Test for until() rule method"""
        rule = _Rule(TestAstNode, None) \
            .one_or_more(TOKEN_ONE).until(TOKEN_TWO)
        # Happy case
        tokens = self.generate_list_of_tokens([TOKEN_ONE, TOKEN_ONE, TOKEN_TWO, TOKEN_TWO])
        result, _ = rule.build_tree_from(tokens)
        self.assert_tokens_variants(result.children[0], [TOKEN_ONE, TOKEN_ONE])

    def test_nested_rules(self):
        """Test for nested rules"""
        ## TODO: implement

if __name__ == '__main__':
    debug.trace_current_context()
    pytest.main([__file__])
