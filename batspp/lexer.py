#!/usr/bin/env python3
#
# Lexer module
#
# This is responsible for breaking
# a sentence/text apart into tokens for Batspp
#


"""
Lexer module

This is responsible for breaking
a sentence/text apart into tokens for Batspp
"""


# Standard packages
import re
from enum import Enum


# Installed packages
from mezcla import debug


# Local modules
import exceptions


class Data:
    """Data class"""

    def __init__(self,
                 text_line:str = '',
                 line:int = None,
                 column:int = None) -> None:
        self.text_line = text_line
        self.line = line
        self.column = column


class TokenType(Enum):
    """Token types enum"""
    # Single-character token types
    PESO = '$'
    # Reserved words
    SETUP = 'setup'
    TEARDOWN = 'teardown'
    TEST = 'test'
    POINTER = ' of '
    CONTINUATION = 'continuation'
    # Misc
    TEXT = 'TEXT'
    EMPTY = 'EMPTY'
    EOF = 'EOF' # end of file


class Token:
    """
    Token class
    """

    def __init__(self,
                 ttype:str,
                 tvalue:any,
                 data: Data = Data()):
        # NOTE: extra "t" in ttype and tvalue
        #       avoids redefine the built-in 'type'
        self.type = ttype
        self.value = tvalue
        self.data = data


class TextHandler:
    """
    This is used to handle text
    """

    def __init__(self, content:str):
        self.lines = content.splitlines()
        self.line = 0
        self.column = 0

    def is_column_safe(self) -> bool:
        """Check column limits"""
        return self.column < len(self.lines[self.line])

    def is_line_safe(self) -> bool:
        """Check line limits"""
        return self.line < len(self.lines)

    def get_rest_line(self) -> str:
        """Get line from actual column to end of line"""

        result = None

        if self.is_line_safe() and self.is_column_safe():
            result = self.lines[self.line][self.column:]

        return result

    def get_current_line(self):
        """Returns line"""
        return self.lines[self.line] if self.is_line_safe() else None

    def advance_column(self, step:int=1) -> None:
        """Advance text column"""
        self.column += step
        if not self.is_column_safe():
            self.advance_line()

    def advance_line(self) -> None:
        """Advance text line"""
        self.line += 1
        self.column = 0


class Lexer:
    """
    This is responsible for breaking
    a sentence/text apart into tokens for Batspp
    """

    def __init__(self, embedded_tests=False):
        self.embedded_tests = embedded_tests

    def tokenize(self, text: TextHandler) -> list:
        """Tokenize text"""
        ## TODO: refactor this copypaste caos
        ## TODO: analyze how much execution time takes regex

        assert isinstance(text, TextHandler), 'Invalid text; must be a TextHandler'

        # Set comments delimiter for embedded tests
        indent = r'^# *' if self.embedded_tests else r'^ *'

        # Tokenize
        # For convention each token is responsible for the space that precedes it
        # NOTE: we dont use full regex to have more control and handle exceptions better
        result = []
        while text.is_line_safe():

            data = Data(text_line=text.get_current_line(),
                        line = text.line + 1,
                        column = text.column + 1)

            # Tokenize empty lines
            if text.get_current_line() == '':
                while text.get_current_line() == '':
                    text.advance_line()
                result.append(Token(TokenType.EMPTY, None, data))
                continue

            # Skip double comment delimiter
            if re.match(r'^##', text.get_rest_line()):
                text.advance_line()
                continue

            # Tokenize peso
            match = re.match(fr'{indent}\$', text.get_rest_line())
            if match:
                text.advance_column(match.span()[1])
                result.append(Token(TokenType.PESO, match.group(), data))
                continue

            # Tokenize test
            match = re.match(r'^# *[Tt]est(?: +|$)', text.get_rest_line())
            if match:
                text.advance_column(match.span()[1])
                result.append(Token(TokenType.TEST, match.group(), data))
                continue

            # Tokenize setup
            match = re.match(r'^# *[Ss]etup(?: +|$)', text.get_rest_line())
            if match:
                text.advance_column(match.span()[1])
                result.append(Token(TokenType.SETUP, match.group(), data))
                continue

            # Tokenize teardown
            match = re.match(r'^# *[Tt]eardown(?: +|$)', text.get_rest_line())
            if match:
                text.advance_column(match.span()[1])
                result.append(Token(TokenType.TEARDOWN, match.group(), data))
                continue

            # Tokenize continuation
            match = re.match(r'^# *(?:[Cc]ontinue|[Cc]ontinuation)(?: +|$)', text.get_rest_line())
            if match:
                text.advance_column(match.span()[1])
                result.append(Token(TokenType.CONTINUATION, match.group(), data))
                continue

            # Tokenize pointer
            match = re.match(r'^ *of', text.get_rest_line())
            if match:
                text.advance_column(match.span()[1])
                result.append(Token(TokenType.POINTER, match.group(), data))
                continue

            # Tokenize text
            match = re.match(r'^[^#]+$', text.get_rest_line())
            if match:
                text.advance_column(match.span()[1])
                result.append(Token(TokenType.TEXT, match.group(), data))
                continue

            # Skip comment delimiter
            if re.match(r'^ *#', text.get_current_line()):
                text.advance_line()
                continue

            exceptions.error(message='Invalid syntax',
                             text_line=data.text_line,
                             line=data.line,
                             column=data.column)

        # Tokenize End of file
        result.append(Token(TokenType.EOF, None, None))

        debug.trace(7, 'lexer.tokenize() =>')
        for token in result:
            if token:
                debug.trace(7, (f'token: type={token.type}, '
                                f'line={token.data.line if token.data else None}, '
                                f'column={token.data.column if token.data else None}, '
                                f'value={token.value}'))

        return result
