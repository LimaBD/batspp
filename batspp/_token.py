#!/usr/bin/env python3
#
# Token module
#

"""Token module"""

# Standard packages
## NOTE: this is empty for now

# Installed packages
## NOTE: this is empty for now

# Local packages
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )

# Token variants
#
# NOTE: we dont use enum to get a more
#       readable code in the parser module.
#
# Single-character token variants
PESO = 'PESO'
GREATER = 'GREATER'
# Reserved words tokens
SETUP = 'setup'
GLOBAL = 'global'
TEARDOWN = 'teardown'
TEST = 'test'
POINTER = ' of '
CONTINUATION = 'continuation'
ASSERT_EQ = 'ASSERT_EQ' # "=>"
ASSERT_NE = 'ASSERT_NE' # "=>"
# Misc tokens
TEXT = 'TEXT'
EOF = 'EOF'
# NOTE: to be deprecated
NEW_LINE = 'NEW_LINE' ## TODO: unify to TEXT token
MINOR = 'MINOR'

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

class Token:
    """
    Token class
    """

    def __init__(
            self,
            variant: str,
            value: any,
            data: TokenData = TokenData(),
            ) -> None:
        self.variant = variant
        self.value = value
        self.data = data

    def __repr__(self) -> str:
        return f'Token({self.variant.upper()})'

if __name__ == '__main__':
    warning_not_intended_for_cmd()
