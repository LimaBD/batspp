#!/usr/bin/env python3
#
# Abstact syntax tree (AST) nodes module
#


"""Abstact syntax tree (AST) nodes module"""


# Standard packages
from enum import Enum

# Installed packages
## NOTE: this is empty for now

# Local packages
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )
from batspp._token import TokenData


class AST:
    """
    Abstract Syntax Tree interface for Batspp
    """

    def __init__(
            self,
            data: TokenData = TokenData(),
            ) -> None:
        self.data = data


class AssertionType(Enum):
    """
    Assertion type enum
    """
    OUTPUT = 'output'
    EQUAL = 'equal'
    NOT_EQUAL = 'not_equal'


class Assertion(AST):
    """
    AST node for assertion
    """

    def __init__(
            self,
            atype: AssertionType,
            setup_commands: list = None,
            actual: str = '',
            expected: str = '',
            data: TokenData = TokenData(),
            ) -> None:
        super().__init__(data)
        self.atype = atype
        self.setup_commands = setup_commands
        self.actual = actual
        self.expected = expected


class Test(AST):
    """
    AST node for test
    """

    def __init__(
            self,
            reference: str = '',
            assertions: list = None,
            data: TokenData = TokenData(),
            ) -> None:
        super().__init__(data)
        self.reference = reference
        self.assertions = assertions if assertions else []


class TestsSuite(AST):
    """
    AST node for test suite
    """

    def __init__(
            self,
            tests: list,
            setup_commands: list = None,
            teardown_commands: list = None,
            data: TokenData = TokenData(),
            ) -> None:
        super().__init__(data)
        self.tests = tests
        self.setup_commands = setup_commands
        self.teardown_commands = teardown_commands


if __name__ == '__main__':
    warning_not_intended_for_cmd()
