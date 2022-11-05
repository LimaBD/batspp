#!/usr/bin/env python3
#
# Token module
#


"""Token module"""


# Standard packages
from enum import Enum

# Installed packages
## NOTE: this is empty for now

# Local packages
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )


class TokenData:
    """Data class for token"""

    def __init__(
            self,
            text_line:str = '',
            line:int = None,
            column:int = None,
            ) -> None:
        self.text_line = text_line
        self.line = line
        self.column = column

    def __str__(self):
        return (
            f'TokenData(text_line={self.text_line},\n'
            f'\t          line={self.line},\n'
            f'\t          column={self.column})'
            )


class TokenVariant(Enum):
    """Token variants enum"""
    # Single-character token variants
    PESO = '$'
    GREATER = '>'
    NEW_LINE = '\n'
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

    def __init__(
            self,
            variant: TokenVariant,
            value:any,
            data: TokenData = TokenData(),
            ) -> None:
        self.variant = variant
        self.value = value
        self.data = data

    def __str__(self):
        return (
            f'Token(variant={self.variant},\n'
            f'      value={self.value},\n'
            f'      data={self.data})'
            )


if __name__ == '__main__':
    warning_not_intended_for_cmd()
