#!/usr/bin/env python3
#
# Abstact syntax tree (AST) nodes module
#

"""Abstact syntax tree (AST) nodes module"""

# Standard packages
## NOTE: this is empty for now

# Installed packages
## NOTE: this is empty for now

# Local packages
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )
from batspp._token import (
    Token,
    )

class ASTnode:
    """Abstract Syntax Tree node for Batspp"""

    def __init__(self) -> None:
        """Initialize AST node"""
        pass

    @property
    def line(self) -> int:
        """Return the line number of the node"""
        # Search in children the lower line number
        child_lines = []
        for child in self.__dict__.values():
            if isinstance(child, ASTnode) or isinstance(child, Token):
                child_lines.append(child.line)
            elif isinstance(child, list):
                for subchild in child:
                    if subchild is not None:
                        child_lines.append(subchild.line)
        child_lines = [line for line in child_lines if line is not None]
        if child_lines:
            return min(child_lines)
        raise Exception('ASTnode.line: no line number found')

class Text(ASTnode):
    """Text node"""

    def __init__(self, text: Token) -> None:
        """Initialize AST node"""
        self.text = text

class MultilineText(ASTnode):
    """Multiline text node"""

    def __init__(self, text_lines: list) -> None:
        """Initialize AST node"""
        self.text_lines = text_lines # Tokens or Text nodes

class CommandExtension(ASTnode):
    """Command extension node"""

    def __init__(self, greater: Token, command: Token) -> None:
        """Initialize AST node"""
        self.greater = greater
        self.command = command

class Command(ASTnode):
    """Command node"""

    def __init__(self, peso: Token, command: Token, extensions: list=None) -> None:
        """Initialize AST node"""
        self.peso = peso
        self.command = command
        self.extensions = extensions if extensions else []

class ArrowAssertion(ASTnode):
    """Arrow EQ assertion node"""

    def __init__(self, actual: Token, assertion: Token, expected_lines: list) -> None:
        """Initialize AST node"""
        self.actual = actual
        self.assertion = assertion
        self.expected_lines = expected_lines

class CommandAssertion(ASTnode):
    """Command assertion node"""

    def __init__(self, command: Command, expected: MultilineText) -> None:
        """Initialize AST node"""
        self.command = command
        self.expected = expected

class Assertion(ASTnode):
    """Assertion node"""

    def __init__(self, assertion: 'CommandAssertion|ArrowAssertion') -> None:
        """Initialize AST node"""
        self.assertion = assertion

class ContinuationReferencePrefix(ASTnode):
    """Continuation reference prefix node"""

    def __init__(self, continuation: Token, pointer: Token) -> None:
        """Initialize AST node"""
        self.continuation = continuation
        self.pointer = pointer

class TestReference(ASTnode):
    """Test reference node"""
    __test__ = False # This is not a test case

    def __init__(self, pointer: 'Token|ContinuationReferencePrefix', reference: Token) -> None:
        """Initialize AST node"""
        self.pointer = pointer
        self.reference = reference

class SetupReference(ASTnode):
    """Setup reference node"""

    def __init__(self, setup: Token, pointer: Token, reference: Token) -> None:
        """Initialize AST node"""
        self.setup = setup
        self.pointer = pointer
        self.reference = reference

class StandaloneCommands(ASTnode):
    """Standalone commands node"""

    def __init__(self, commands: list=[]) -> None:
        self.commands = commands

class Setup(ASTnode):
    """Setup node"""

    def __init__(self, reference: SetupReference, commands: StandaloneCommands) -> None:
        """Initialize AST node"""
        self.reference = reference
        self.commands = commands

class Test(ASTnode):
    """Test node"""
    __test__ = False # This is not a test case

    def __init__(self, reference: TestReference, setup_assertions: list) -> None:
        """Initialize AST node"""
        self.reference = reference
        self.setup_assertions = setup_assertions

class GlobalSetup(ASTnode):
    """Global setup node"""

    def __init__(self, globalt:Token, setup: Token, commands: StandaloneCommands) -> None:
        """Initialize AST node"""
        self.globalt = globalt
        self.setup = setup
        self.one_time_commands = StandaloneCommands()
        self.commands = commands

class GlobalTeardown(ASTnode):
    """Global teardown node"""

    def __init__(self, globalt:Token, teardown: Token, commands: StandaloneCommands) -> None:
        """Initialize AST node"""
        self.globalt = globalt
        self.teardown = teardown
        self.commands = commands

class TestOrSetup(ASTnode):
    """Test or setup node"""
    __test__ = False # This is not a test case

    ## TODO: remove all ast nodes like this that only are used to store one child node

    def __init__(self, child: 'Test|Setup') -> None:
        """Initialize AST node"""
        self.child = child

class TestSuite(ASTnode):
    """Test suite node"""
    __test__ = False # This is not a test case

    def __init__(
            self,
            global_setup: GlobalSetup,
            tests_or_setups: list,
            global_teardown: GlobalTeardown,
            eof: Token,
            ) -> None:
        """Initialize AST node"""
        self.constants: Constants = None # This is added later, not during construction.
        self.global_setup = global_setup
        self.tests_or_setups = tests_or_setups
        self.global_teardown = global_teardown
        self.eof = eof

class SetupAssertion(ASTnode):
    """Setup assertion node"""

    def __init__(self, setup: Setup, assertion: Assertion) -> None:
        """Initialize AST node"""
        self.setup = setup
        self.assertion = assertion

class Constants(ASTnode):
    """Constants node"""

    def __init__(self, constants: list) -> None:
        """Initialize AST node"""
        self.constants = constants

if __name__ == '__main__':
    warning_not_intended_for_cmd()
