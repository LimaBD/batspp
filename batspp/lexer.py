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


class Tags(Enum):
    """Tags enum"""
    EOF = '<EOF>' # expected output EOF
    END = '<END>' # end of assertion
    BLANK = '<BLANK>' # blank line


class TokenData:
    """Data class for token"""

    def __init__(self,
                 text_line:str = '',
                 line:int = None,
                 column:int = None) -> None:
        self.text_line = text_line
        self.line = line
        self.column = column

    def __str__(self):
        return (f'TokenData(text_line={self.text_line},\n'
                f'\t          line={self.line},\n'
                f'\t          column={self.column})')


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
    ASSERT_EQ = '=>'
    ASSERT_NE = '=/>'
    # Misc
    TEXT = 'TEXT'
    MINOR = 'MINOR' # unimportant tokens that cannot be ignored
    EOF = 'EOF' # end of file


class Token:
    """
    Token class
    """

    def __init__(self,
                 ttype:str,
                 tvalue:any,
                 data: TokenData = TokenData()):
        # NOTE: extra "t" in ttype and tvalue
        #       avoids redefine the built-in 'type'
        self.type = ttype
        self.value = tvalue
        self.data = data

    def __str__(self):
        return (f'Token(type={self.type},\n'
                f'      value={self.value},\n'
                f'      data={self.data})')


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
        self.extra_indent = ''
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

            data = TokenData(text_line=self.text.get_current_line(),
                             line = self.text.line + 1,
                             column = self.text.column + 1)

            # Tokenize lines with double comments as minor token
            match = re.match(r'^##', self.text.get_current_line())
            if match:
                self.text.advance_line()
                self.append_minor_token(Token(TokenType.MINOR, match.group(), data))
                continue

            # Tokenize empty lines
            match = re.match(r'^ *$', self.text.get_current_line())
            if match:
                self.text.advance_line()
                self.append_minor_token(Token(TokenType.MINOR, match.group(), data))
                continue

            # Tokenize peso
            match = re.match(r' *\$', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(TokenType.PESO, match.group(), data))
                continue

            # Tokenize test
            match = re.match(r'^# *[Tt]est(?: +|$)', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(TokenType.TEST, match.group(), data))
                continue

            # Tokenize setup
            match = re.match(r'^# *[Ss]etup(?: +|$)', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(TokenType.SETUP, match.group(), data))
                continue

            # Tokenize teardown
            match = re.match(r'^# *[Tt]eardown(?: +|$)', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(TokenType.TEARDOWN, match.group(), data))
                continue

            # Tokenize continuation
            match = re.match(r'^# *(?:[Cc]ontinue|[Cc]ontinuation)(?: +|$)', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(TokenType.CONTINUATION, match.group(), data))
                continue

            # Tokenize tags EOF and END
            if self.text.get_rest_line().startswith((Tags.END.value, Tags.EOF.value)):
                self.text.advance_column(5)
                self.append_token(Token(TokenType.MINOR, None, data))
                continue

            # Tokenize BLANK tag
            if self.text.get_rest_line().startswith(Tags.BLANK.value):
                self.text.advance_column(len(Tags.BLANK.value))
                self.append_token(Token(TokenType.TEXT, '\n', data))
                continue

            # Tokenize pointer
            match = re.match(r'^ *of', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(TokenType.POINTER, match.group(), data))
                continue

            # Tokenize assert equal
            match = re.match(r' *=> *', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(TokenType.ASSERT_EQ, match.group(), data))
                continue

            # Tokenize assert not equal
            match = re.match(r' *=/> *', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(TokenType.ASSERT_NE, match.group(), data))
                continue

            # Tokenize text
            match = re.match(r'^[^#]+?(?==>|=/>|$)', self.text.get_rest_line())
            if match:
                self.text.advance_column(match.span()[1])
                self.append_token(Token(TokenType.TEXT, match.group(), data))
                continue

            # Tokenize comments as minor token
            match = re.match(r'^ *#.*?$', self.text.get_current_line())
            if match:
                self.text.advance_line()
                self.append_minor_token(Token(TokenType.MINOR, None, data))
                continue

            exceptions.error(message='invalid syntax',
                             text_line=data.text_line,
                             line=data.line,
                             column=data.column)

        # Tokenize End of file
        self.append_token(Token(TokenType.EOF, None, None))

    def tokenize(self, text: str, embedded_tests:bool=False) -> list:
        """Tokenize text"""

        # Clean global class values
        #
        # This is useful if is needed to reuse
        # the same instance of this class
        self.extra_indent = ''
        self.text = TextLiner(text)
        self.tokens = []

        # Set extra indent and remove not commented
        # lines because we only focus on the
        # commented lines if there are embedded tests
        if embedded_tests:
            self.extra_indent = r'#'
            text = re.sub(r'^[^#\n]+?$', '\n', text)

        # Tokenize text
        self.extract_tokens()

        debug.trace(7, f'Lexer.tokenize(text={text}, embedded_tests={embedded_tests})')
        return self.tokens
