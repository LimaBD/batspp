#!/usr/bin/env python3
#
# Parser module
#
# This module is responsible for building
# an abstract syntax tree (AST) for Batspp
#
## TODO: solve: Setup and Continue referenced before
##       assignment should print the correct line, not the next.


"""
Parser module

This module is responsible for building
an Abstract Syntax Tree (AST) for Batspp
"""


# Standard packages
## NOTE: this is empty for now


# Installed packages
from mezcla import debug


# Local packages
from batspp._exceptions import error
from batspp._token import (
    TokenType, Token,
    )
from batspp._ast_nodes import (
    AST, TestsSuite, Test,
    Assertion, AssertionType,
    )


class Parser:
    """
    This is responsible for building an
    abstract syntax tree (AST) for Batspp
    """

    def __init__(self) -> None:
        # Global states variables
        self.tokens = []
        self.index = 0
        self.last_pointer = ''
        self.test_nodes = []
        self.setup_commands_stack = []
        self.teardown_commands_stack = []
        self.embedded_tests = False

    def reset_global_state_variables(self) -> None:
        """Reset global states variables"""
        self.__init__()

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
            error(
                message=f'Expected {token_type} but founded {current_token.type}',
                text_line=current_token.data.text_line,
                line=current_token.data.line,
                )

    def is_command_next(self) -> bool:
        """
        Check if a command token pattern is next
        command : PESO TEXT
        """

        result = False
        first = self.get_current_token()
        second = self.peek_token(1)

        if second is not None:
            result = (
                first.type is TokenType.PESO
                and second.type is TokenType.TEXT
                )

        debug.trace(7, (
            f'parser.is_command_next() =>'
            f' next tokens types: {first} {second}'
            f' => {result}'
            ))
        return result

    def is_setup_command_next(self) -> bool:
        """
        Check for setup command token pattern next
        setup : command ^[TEXT]
        """
        ## TODO: refactor using not is_command_assertion_next

        result = False
        is_command = self.is_command_next()
        third_token = self.peek_token(2)

        if third_token is not None:
            result = (
                is_command
                and third_token.type is not TokenType.TEXT
                )

        debug.trace(7, (
            'parser.is_setup_command_next() => '
            f'command:{is_command} {third_token}'
            f' => {result}'
            ))
        return result

    def is_command_assertion_next(self) -> bool:
        """
        Check if a command assertion tokens pattern is next
        command_assertion : command TEXT
        """
        result = False
        third_token = self.peek_token(2)

        if third_token:
            result = self.is_command_next() and third_token.type is TokenType.TEXT

        debug.trace(7, (
            f'parser.is_command_assertion_next() => {result}'
            ))
        return result

    def is_arrow_assertion_next(self) -> bool:
        """
        Check if a arrow assertion tokens pattern is next
        arrow_assertion : TEXT (ASSERT_EQ|ASSERT_NE) TEXT
        """
        result = False
        first_token = self.get_current_token()
        second_token = self.peek_token(1)
        third_token = self.peek_token(2)

        if first_token and second_token and third_token:
            result = (
                first_token.type is TokenType.TEXT
                and second_token.type in [TokenType.ASSERT_EQ, TokenType.ASSERT_NE]
                and third_token.type is TokenType.TEXT
                )
        debug.trace(7, (
            f'parser.is_arrow_assertion_next() => {result}'
            ))
        return result

    def is_assertion_next(self) -> bool:
        """
        Check if a assertion tokens pattern is next
        """
        result = self.is_command_assertion_next() or self.is_arrow_assertion_next()
        debug.trace(7, (
            f'parser.is_assertion_next() => {result}'
            ))
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
        # Are break into setup commands or assertion nodes
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
            error(
                message='Continuation without test assigned',
                text_line=data.text_line,
                line=data.line,
                column=data.column,
                )

        self.break_setup_assertion(pointer)

    def break_setup_assertion(self, pointer:int = '') -> None:
        """
        Process and break block test
        into setup commands and assertion AST nodes and set POINTER as pointer
        """
        debug.trace(7, f'parser.break_setup_assertion(pointer={pointer})')

        # Separate/break blocks into setup commands and assertion nodes

        assert pointer, 'Invalid empty pointer'

        while True:
            if self.is_setup_command_next():
                # Only setups can be present on a
                # block assertion, not teardowns
                self.append_setup_commands(pointer)
            elif self.is_assertion_next():
                self.build_assertion(pointer)
            else:
                break

    def append_setup_commands(self, pointer:str='') -> None:
        """
        Append Setup commands and set POINTER as pointer
        """
        debug.trace(7, f'parser.append_setup_commands(pointer={pointer})')

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

        commands = self.extract_setup_commands(data)

        # Push new setup commands to the stack,
        # this must contains an pointer to later
        # assign this to an assertion
        self.setup_commands_stack.append((pointer, commands))

    def append_teardown_commands(self) -> None:
        """
        Append teardown commands to stack
        """
        debug.trace(7, 'parser.append_teardown_commands()')

        # Set debug data
        data = self.get_current_token().data

        self.eat(TokenType.TEARDOWN)
        commands = self.extract_setup_commands(data)

        self.teardown_commands_stack.append(commands)

    def extract_setup_commands(self, data):
        """
        Extract setup commands from blocks of setup commands,
        also raise exception if block of commands are empty.
        """
        commands = []

        while self.is_setup_command_next():
            self.eat(TokenType.PESO)
            commands.append(self.get_current_token().value)
            self.eat(TokenType.TEXT)

        if not commands:
            error(
                message = 'Setup cannot be empty',
                text_line = data.text_line,
                line = data.line,
                column = data.column,
                )

        return commands

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
        node = Assertion(
            atype=atype,
            setup_commands=None,
            actual=actual,
            expected=expected,
            data=data,
            )

        # Assign setups from the stack with
        # the same pointer as the assertion
        node.setup_commands = self.pop_setup_commands(pointer=pointer)

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
            error(
                message=f'Assertion "{pointer}" referenced before assignment.',
                text_line=node.data.text_line,
                line=node.data.line,
                column=None,
                )

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

            # Process next tokens as a test directive pattern
            elif token_type is TokenType.TEST:
                self.build_test()

            # Process next tokens as a continuation directive pattern
            #
            # Continuation pattern are brak
            # into Setup and Assertions nodes
            elif token_type is TokenType.CONTINUATION:
                self.break_continuation()

            # Process next tokens as a setup directive pattern
            elif token_type is TokenType.SETUP:
                self.append_setup_commands()

            # Process next tokens as teardown directive pattern
            elif token_type is TokenType.TEARDOWN:
                self.append_teardown_commands()

            # Create new test node for standlone commands and assertions
            elif self.is_command_next() or self.is_assertion_next():
                self.build_test(f'test of line {current_token.data.line}')

            # (Only when embedded_tests!) skip standlone text tokens
            elif self.embedded_tests and token_type is TokenType.TEXT:
                self.eat(TokenType.TEXT)

            # Finish
            else:
                break

        # The last token always should be an EOF
        self.eat(TokenType.EOF)

        # Set global global setup for test suite
        setup_commands = self.pop_setup_commands(pointer='')

        # Finishing the parsing, cannot be remaining setups on stack
        if self.setup_commands_stack:
            first_invalid = self.setup_commands_stack[0]
            error(
                message=f'Setup "{first_invalid.pointer}" referenced before assignment.',
                text_line=first_invalid.data.text_line,
                line=first_invalid.data.line,
                column=None,
                )

        result = TestsSuite(
            self.test_nodes,
            setup_commands = setup_commands,
            teardown_commands = self.teardown_commands_stack,
            )
        debug.trace(7, f'parser.build_tests_suite() => {result}')
        return result

    def pop_setup_commands(self, pointer: str) -> list:
        """
        Pop setup commands from stack with same POINTER,
        if several setups commands blocks are founded, unify all into one
        """
        result = []

        # Get commands from stack with same pointer
        for stack_pointer, commands in self.setup_commands_stack:
            if stack_pointer == pointer:
                result += commands
                self.setup_commands_stack.remove((stack_pointer, commands))

        return result

    def parse(
            self,
            tokens: list,
            embedded_tests:bool=False,
            ) -> AST:
        """
        Builds an Abstract Syntax Tree (AST) from TOKENS list
        """
        assert tokens, 'Tokens list cannot be empty'
        assert tokens[-1], 'Last token should be EOF'

        self.reset_global_state_variables()
        self.tokens = tokens
        self.embedded_tests = embedded_tests

        result = self.build_tests_suite()

        debug.trace(7, f'Parser.parse() => {result}')
        return result
