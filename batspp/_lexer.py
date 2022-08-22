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
from re import (
    match as re_match,
    sub as re_sub,
    MULTILINE as re_MULTILINE,    
    )
from enum import Enum


# Installed packages
from mezcla import debug


# Local packages
from batspp._exceptions import error
from batspp._token import (
    TokenData, TokenType, Token,
    )


class Tags(Enum):
    """Tags enum"""
    EOF = '<EOF>' # expected output EOF
    END = '<END>' # end of assertion
    BLANK = '<BLANK>' # blank line


class TextLiner:
    """
    This provides functionality to process text line per line
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
        """Returns full current line"""
        return self.lines[self.line] if self.is_line_safe() else None

    def advance_column(self, step:int=1) -> None:
        """Advance column N STEP columns on text"""
        self.column += step
        if not self.is_column_safe():
            self.advance_line()

    def advance_line(self) -> None:
        """Advance to the next text line"""
        self.line += 1
        self.column = 0


class Lexer:
    """
    This is responsible for breaking
    a sentence/text apart into tokens for Batspp
    """

    def __init__(self) -> None:
        self.text = None
        self.tokens = []

    def append_token(self, token: Token) -> None:
        """
        Appends TOKEN, this provides a debug trace
        """
        debug.trace(7, f'Lexer.append_token(\ntoken={token}\n)')
        self.tokens.append(token)

    def append_minor_token(self, token: Token) -> None:
        """
        appends minor TOKEN only if these are not a previus MINOR token.
        this avoids have N unnecesary MINOR tokens.
        """

        assert token.type is TokenType.MINOR, 'wrong token type, must be a MINOR'

        if self.tokens and self.tokens[-1].type is TokenType.MINOR:
            debug.trace(7, f'Lexer.append_minor_token(token={token}) -> kicked!')
            return

        self.append_token(token)

    def extract_tokens(self):
        """Extract all tokens from text"""
        ## TODO: refactor this copypaste caos
        ## TODO: analyze how much execution time takes regex
        ## TODO; implement usage of extra_indent to comments embedded tests

        # For convention each token is responsible
        # (at least) for the space that precedes it
        #
        # NOTE: we dont use full regex to have more
        #       control and handle exceptions better
        while self.text.is_line_safe():

            data = TokenData(
                text_line = self.text.get_current_line(),
                line = self.text.line + 1,
                column = self.text.column + 1,
                )

            # Tokenize lines with double comments as minor token
            match = re_match(r'^##', self.text.get_current_line())
            if match:
                self.text.advance_line()
                self.append_minor_token(Token(
                    TokenType.MINOR,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize empty lines
            match = re_match(r'^ *$', self.text.get_current_line())
            if match:
                self.text.advance_line()
                self.append_minor_token(Token(
                    TokenType.MINOR,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize peso
            match = re_match(r' *\$', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(
                    TokenType.PESO,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize test
            match = re_match(r'^# *[Tt]est(?: +|$)', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(
                    TokenType.TEST,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize setup
            match = re_match(r'^# *[Ss]etup(?: +|$)', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(
                    TokenType.SETUP,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize teardown
            match = re_match(r'^# *[Tt]eardown(?: +|$)', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(
                    TokenType.TEARDOWN,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize continuation
            match = re_match(r'^# *(?:[Cc]ontinue|[Cc]ontinuation)(?: +|$)', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(
                    TokenType.CONTINUATION,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize tags EOF and END
            if self.text.get_rest_line().startswith((Tags.END.value, Tags.EOF.value)):
                self.text.advance_column(5)
                self.append_token(Token(
                    TokenType.MINOR,
                    None,
                    data,
                    ))
                continue

            # Tokenize BLANK tag
            if self.text.get_rest_line().startswith(Tags.BLANK.value):
                self.text.advance_column(len(Tags.BLANK.value))
                self.append_token(Token(
                    TokenType.TEXT,
                    '\n',
                    data,
                    ))
                continue

            # Tokenize pointer
            match = re_match(r'^ *of', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(
                    TokenType.POINTER,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize assert equal
            match= re_match(r' *=> *', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(
                    TokenType.ASSERT_EQ,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize assert not equal
            match = re_match(r' *=\/> *', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(
                    TokenType.ASSERT_NE,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize text
            match = re_match(r'^[^#]+?(?==>|=/>|$)', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(
                    TokenType.TEXT,
                    match.group(),
                    data,
                    ))
                continue

            # Tokenize comments as minor token
            match = re_match(r'^ *#.*?$', self.text.get_current_line())
            if match:
                self.text.advance_line()
                self.append_minor_token(Token(
                    TokenType.MINOR,
                    None,
                    data,
                    ))
                continue

            error(
                message='invalid syntax',
                text_line=data.text_line,
                line=data.line,
                column=data.column,
                )

        # Tokenize End of file
        self.append_token(Token(TokenType.EOF, None, None))

    def tokenize(self, text: str, embedded_tests:bool=False) -> list:
        """Tokenize text"""

        # Format embedded comment tests into normal batspp tests
        if embedded_tests:
            # 1st remove not commented lines
            text = re_sub(r'^[^#]+?$', '\n', text, flags=re_MULTILINE)
            # 2nd remove comment delimiter '#' from commented lines
            ## TODO: remove redundancy of directives
            text = re_sub(r'^# ?(?! *(?:[Tt]est|[Cc]continue|[Cc]ontinuation|[Ss]etup|[Tt]eardown))', '', text, flags=re_MULTILINE)
            debug.trace(7, f'lexer.tokenize() => formated embedded tests to:\n{text}')

        # Clean global class values
        #
        # This is useful if is needed to reuse
        # the same instance of this class
        self.text = TextLiner(text)
        self.tokens = []

        # Tokenize text
        self.extract_tokens()

        debug.trace(7,
            f'Lexer.tokenize(text={text}, embedded_tests={embedded_tests})'
            )
        return self.tokens
