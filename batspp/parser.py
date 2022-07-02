#!/usr/bin/env python3
#
# Parser module
#
# This module is responsible for building
# an abstract syntax tree (AST) for Batspp
#
## TODO: parse teardown blocks
## TODO: solve: Setup and Continue referenced before
##       assignment should print the correct line, not the next.


"""
Parser module

This module is responsible for building
an Abstract Syntax Tree (AST) for Batspp
"""


# Standard packages
from enum import Enum


# Installed packages
from mezcla import debug


# Local modules
import exceptions
from lexer import Data, TokenType, Token


class AST:
    """Abstract Syntax Tree interface for Batspp"""

    def __init__(self, data: Data = Data()) -> None:
        self.data = data


class Setup(AST):
    """
    AST node for setup
    """

    def __init__(self,
                 commands:list = None,
                 data: Data = Data()) -> None:
        super().__init__(data)
        self.commands = commands if commands else []


class AssertionType(Enum):
    """Assertion type enum"""
    OUTPUT = 'output'
    EQUAL = 'equal'
    NOT_EQUAL = 'not_equal'


class Assertion(AST):
    """
    AST node for assertion
    """

    def __init__(self,
                 atype: AssertionType,
                 setup: Setup = None,
                 actual: str = '',
                 expected: str = '',
                 data: Data = Data()) -> None:
        super().__init__(data)
        self.atype = atype
        self.setup = setup
        self.actual = actual
        self.expected = expected


class Test(AST):
    """
    AST node for test
    """

    def __init__(self,
                 pointer: str = '',
                 assertions: list = None,
                 data: Data = Data()) -> None:
        super().__init__(data)
        self.pointer = pointer
        self.assertions = assertions if assertions else []


class TestsSuite(AST):
    """
    AST node for test suite
    """

    def __init__(self,
                 setup: Setup,
                 tests: list,
                 data: Data = Data()) -> None:
        super().__init__(data)
        self.setup = setup
        self.tests = tests


class Parser:
    """
    This is responsible for building an
    abstract syntax tree (AST) for Batspp
    """

    def __init__(self) -> None:
        self.tokens = []
        self.index = 0
        self.last_pointer = ''
        self.test_nodes = []
        self.setup_stack = []

    def get_current_token(self) -> Token:
        """Returns current token"""

        result = self.peek_token(0)

        debug.trace(7, f'parser.get_current_token() => {result}')
        return result

    def peek_token(self, number:int =1) -> Token:
        """Peek next NUMBER of tokens ahead"""

        moved_index = self.index + number

        result = None

        # We dont get the last token because should be EOF
        if moved_index < len(self.tokens):
            result = self.tokens[moved_index]

        debug.trace(7, f'parser.peek_token(number={number}) => {result}')
        return result

    def eat(self, token_type:str) -> None:
        """
        Compare current token type with TOKEN_TYPE and
        if matchs, advance token otherwise raise exception
        """
        debug.trace(7, f'parser.eat(token_type={token_type})')

        assert token_type, 'invalid token_type'

        current_token = self.get_current_token()

        if current_token.type is token_type:
            self.index += 1
        else:
            exceptions.error(message=(f'Expected {token_type} but '
                                      f'founded {current_token.type}'),
                             text_line=current_token.data.text_line,
                             line=current_token.data.line)

    def is_command_next(self) -> bool:
        """
        Check if a command token pattern is next
        command : PESO TEXT
        """

        result = False
        first = self.get_current_token()
        second = self.peek_token(1)

        if second is not None:
            result = (first.type is TokenType.PESO and
                      second.type is TokenType.TEXT)

        debug.trace(7, (f'parser.is_command_next() =>'
                        f' next tokens types: {first} {second}'
                        f' => {result}'))
        return result

    def is_setup_next(self) -> bool:
        """
        Check if setup tokens pattern is next
        """

        result = False
        is_command = self.is_command_next()
        third_token = self.peek_token(2)

        if third_token is not None:
            result = (is_command and
                      third_token.type is not TokenType.TEXT)

        debug.trace(7, ('parser.is_setup_next() => '
                        f'command:{is_command} {third_token}'
                        f' => {result}'))
        return result

    def is_assertion_next(self) -> bool:
        """
        Check if a assertion tokens pattern is next
        """

        result = False

        first_token = self.get_current_token()
        second_token = self.peek_token(1)
        third_token = self.peek_token(2)

        if first_token and second_token and third_token:

            # Check for command assertion
            if first_token.type is TokenType.PESO:
                result = (second_token.type is TokenType.TEXT and
                          third_token.type is TokenType.TEXT)

            # Check for assert eq or ne
            elif first_token.type is TokenType.TEXT:
                result = (second_token.type in [TokenType.ASSERT_EQ, TokenType.ASSERT_NE] and
                          third_token.type is TokenType.TEXT)

        debug.trace(7, ('parser.is_assertion_next() => '
                        f'command:{first_token} {second_token} {third_token}'
                        f' => {result}'))
        return result

    def build_test(self, pointer:str='') -> None:
        """
        Build and append Test AST node,
        Set POINTER as pointer, otherwise (if empty), search for TEST TEXT tokens
        """
        debug.trace(7, f'parser.build_test(pointer={pointer})')

        # Set debug data
        data = self.get_current_token().data

        # Check for pointer
        if not pointer:
            self.eat(TokenType.TEST)
            pointer = self.get_current_token().value.strip()
            self.last_pointer = pointer
            self.eat(TokenType.TEXT)

        # Add new test node
        node = Test(pointer=pointer, assertions=None, data=data)
        self.test_nodes.append(node)

        self.break_setup_assertion(pointer)

    def break_continuation(self) -> None:
        """
        Process and break continuation block tokens
        """
        debug.trace(7, 'parser.break_continuation()')

        # Continuation blocks e.g.
        #
        #   # Continuation
        #   $ command-setup
        #   $ another-command-setup
        #   $ command
        #   expected-output
        #
        # Are break into setup and assertion nodes
        #
        # If continuation has no pointer token,
        # set pointer to the last test

        data = self.get_current_token().data

        self.eat(TokenType.CONTINUATION)

        pointer = ''

        # Check for pointer
        if self.get_current_token().type is TokenType.POINTER:
            self.eat(TokenType.POINTER)
            pointer = self.get_current_token().value.strip()
            self.eat(TokenType.TEXT)

        # Assign continuation to last test
        elif self.last_pointer:
            pointer = self.last_pointer

        # Otherwise the continuation is invalid
        else:
            exceptions.error(message='Continuation without test assigned',
                             text_line=data.text_line,
                             line=data.line,
                             column=data.column)

        self.break_setup_assertion(pointer)

    def break_setup_assertion(self, pointer:int = '') -> None:
        """
        Process and break block test
        into setup and assertion AST nodes and set POINTER as pointer
        """
        debug.trace(7, f'parser.break_setup_assertion(pointer={pointer})')

        # Separate/break setup and assertion
        # blocks into setup and assertion nodes

        assert pointer, 'Invalid empty pointer'

        while True:
            if self.is_setup_next():
                self.build_setup(pointer)
            elif self.is_assertion_next():
                self.build_assertion(pointer)
            else:
                break

    def build_setup(self, pointer:str='') -> None:
        """
        Build and append Setup AST node and set POINTER as pointer
        """
        debug.trace(7, f'parser.build_setup(pointer={pointer})')

        # Set debug data
        data = self.get_current_token().data

        # Check pointer
        if not pointer:
            self.eat(TokenType.SETUP)

            # Local setups contains pointer
            if self.get_current_token().type is TokenType.POINTER:
                self.eat(TokenType.POINTER)
                pointer = self.get_current_token().value.strip()
                self.eat(TokenType.TEXT)

            # If there are a previus test to the setup,
            # we assign the setup to that test
            elif self.last_pointer:
                pointer = self.last_pointer

            # Otherwise we treat the setup as a
            # global setup (empty pointer)
            else:
                pass

        # Check for commands
        #
        # Setups directives must contains at least one command
        commands = []
        while self.is_setup_next():
            self.eat(TokenType.PESO)
            commands.append(self.get_current_token().value)
            self.eat(TokenType.TEXT)
        if not commands:
            exceptions.error(message='Setup cannot be empty',
                             text_line=data.text_line,
                             line=data.line,
                             column=data.column)

        # Push new setup node to the stack,
        # this must contains an pointer to later
        # assign this to an assertion
        node = [pointer, Setup(commands=commands, data=data)]
        self.setup_stack.append(node)

    def build_assertion(self, pointer:str='') -> None:
        """
        Build and append Assertion AST node and set POINTER as pointer
        """
        debug.trace(7, f'parser.build_assertion(pointer={pointer})')

        # Check pointer
        assert pointer, 'Invalid empty pointer'

        # Set data
        data = self.get_current_token().data

        atype = None
        actual = ''

        # Check for command style assertion
        #
        # These could be:
        # PESO TEXT
        if self.get_current_token().type is TokenType.PESO:
            atype = AssertionType.OUTPUT
            self.eat(TokenType.PESO)
            actual = self.get_current_token().value
            self.eat(TokenType.TEXT)

        # Check for arrow assertion
        #
        # These could be:
        # assertion: TEXT ASSERT_EQ TEXT
        # assertion: TEXT ASSERT_NE TEXT
        elif self.get_current_token().type is TokenType.TEXT:
            actual = self.get_current_token().value
            self.eat(TokenType.TEXT)

            # Check for assertion type
            if self.get_current_token().type is TokenType.ASSERT_EQ:
                atype = AssertionType.EQUAL
                self.eat(TokenType.ASSERT_EQ)
            elif self.get_current_token().type is TokenType.ASSERT_NE:
                atype = AssertionType.NOT_EQUAL
                self.eat(TokenType.ASSERT_NE)

        # Check expected text tokens
        expected = ''
        while self.get_current_token().type is TokenType.TEXT:
            expected += f'{self.get_current_token().value}\n'
            self.eat(TokenType.TEXT)
        expected = expected[:-1] # Remove last newline

        # New assertion node
        node = Assertion(atype=atype,
                         setup=None,
                         actual=actual,
                         expected=expected,
                         data=data)

        # Assign setups from the stack with
        # the same pointer as the assertion
        node.setup = self.pop_setup(pointer=pointer)

        # Assign assertion node to test suite
        #
        # Note that a previus test node should
        # exist to append the new assertion.
        #
        # We loop in reverse because is more probably
        # that the assertion is from the last test,
        # this reduce the number of needed iterations.
        for test in reversed(self.test_nodes):
            if test.pointer == pointer:
                test.assertions.append(node)
                node = None
                break

        # The node cannot remain alone without being assigned to a test
        if node is not None:
            exceptions.error(message=(f'Assertion "{pointer}"'
                                      ' referenced before assignment.'),
                             text_line=node.data.text_line,
                             line=node.data.line,
                             column=None)

    def build_tests_suite(self) -> AST:
        """
        Build AST node for test suite
        """

        # Extract main nodes from tokens list
        # (Test, Setup, Assertion)
        while self.get_current_token() is not None:
            current_token = self.get_current_token()
            token_type = current_token.type

            # Skip minor tokens
            if token_type is TokenType.MINOR:
                self.eat(TokenType.MINOR)
                continue

            # Process next tokens as a test directive pattern
            if token_type is TokenType.TEST:
                self.build_test()

            # Process next tokens as a continuation directive pattern
            #
            # Continuation pattern are brak
            # into Setup and Assertions nodes
            elif token_type is TokenType.CONTINUATION:
                self.break_continuation()

            # Process next tokens as a setup directive pattern
            elif token_type is TokenType.SETUP:
                self.build_setup()

            # Create new test node for standlone commands and assertions
            elif self.is_command_next() or self.is_assertion_next():
                self.build_test(f'test of line {current_token.data.line}')

            # Finish
            else:
                break

        # The last token always should be an EOF
        self.eat(TokenType.EOF)

        # Set global global setup for test suite
        setup = self.pop_setup(pointer='')

        # Finishing the parsing, cannot be remaining setups on stack
        if self.setup_stack:
            first_invalid = self.setup_stack[0]
            exceptions.error(message=(f'Setup "{first_invalid.pointer}"'
                                      ' referenced before assignment.'),
                             text_line=first_invalid.data.text_line,
                             line=first_invalid.data.line,
                             column=None)

        result = TestsSuite(setup, self.test_nodes)
        debug.trace(7, f'parser.build_tests_suite() => {result}')
        return result

    def pop_setup(self, pointer: str) -> Setup:
        """
        Pop setups nodes from stack with same POINTER,
        if several setups are founded, unify all into one
        """
        commands, temp_stack = [], []

        # Get commands from setups with same pointer
        for setup in self.setup_stack:
            if setup[0] == pointer:
                commands += setup[1].commands
            else:
                temp_stack.append(setup)

        # Set setup stack with the remaining setups
        self.setup_stack = temp_stack

        return Setup(commands=commands, data=Data()) if commands else None

    def parse(self, tokens: list) -> AST:
        """
        Builds an Abstract Syntax Tree (AST) from TOKENS list
        """

        # Clean global class values
        #
        # This is useful if is needed to reuse
        # the same instance of this class
        assert tokens, 'Tokens list cannot be empty'
        self.tokens = tokens
        self.index = 0
        self.last_pointer = ''
        self.test_nodes = []
        self.setup_stack = []

        # build AST
        result = self.build_tests_suite()

        debug.trace(7, f'Parser.parse() => {result}')
        return result
