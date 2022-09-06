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
        self.last_reference = ''
        self.tests_ast_nodes_stack = []
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
        result = self.is_command_next() and not self.is_command_assertion_next()
        debug.trace(7, (
            f'parser.is_setup_command_next() => {result}'
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

    def push_test_ast_node(self, reference:str='') -> None:
        """
        Push test AST node to tests stack,
        Set REFERENCE as reference, otherwise (if empty), search for TEST TEXT tokens
        """
        debug.trace(7, f'parser.push_test_ast_node(reference={reference})')

        data = self.get_current_token().data

        if not reference:
            self.eat(TokenType.TEST)
            reference = self.get_current_token().value.strip()
            self.last_reference = reference
            self.eat(TokenType.TEXT)

        self.tests_ast_nodes_stack.append(
            Test(reference=reference, assertions=None, data=data)
            )

        self.break_setup_assertion(reference)

    def pop_tests_ast_nodes(self):
        """
        Pop all tests ast nodes in stack
        """
        debug.trace(7, f'parser.pop_tests_ast_nodes()')
        result = self.tests_ast_nodes_stack
        self.tests_ast_nodes_stack = []
        return result

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
        # If continuation has no reference token,
        # set reference to the last test

        data = self.get_current_token().data

        self.eat(TokenType.CONTINUATION)

        reference = ''

        # Check for reference
        if self.get_current_token().type is TokenType.POINTER:
            self.eat(TokenType.POINTER)
            reference = self.get_current_token().value.strip()
            self.eat(TokenType.TEXT)

        # Assign continuation to last test
        elif self.last_reference:
            reference = self.last_reference

        # Otherwise the continuation is invalid
        else:
            error(
                message='Continuation without test assigned',
                text_line=data.text_line,
                line=data.line,
                column=data.column,
                )

        self.break_setup_assertion(reference)

    def break_setup_assertion(self, reference:int = '') -> None:
        """
        Process and break block test
        into setup commands and assertion AST nodes and set REFERENCE as reference
        """
        debug.trace(7, f'parser.break_setup_assertion(reference={reference})')
        assert reference, 'Invalid empty reference'

        while True:
            if self.is_setup_command_next():
                # Only setups commands can be present on a
                # block assertion, not teardowns
                self.push_setup_commands(reference)
            elif self.is_assertion_next():
                self.build_assertion(reference)
            else:
                break

    def push_setup_commands(self, reference:str='') -> None:
        """
        Push Setup commands to stack and set REFERENCE as reference
        """
        debug.trace(7, f'parser.push_setup_commands(reference={reference})')

        data = self.get_current_token().data

        # Check reference
        if not reference:
            self.eat(TokenType.SETUP)

            # Local setups contains reference
            if self.get_current_token().type is TokenType.POINTER:
                self.eat(TokenType.POINTER)
                reference = self.get_current_token().value.strip()
                self.eat(TokenType.TEXT)

            # If there are a previus test to the setup,
            # we assign the setup to that test
            elif self.last_reference:
                reference = self.last_reference

            # Otherwise we treat the setup as a
            # global setup (empty reference)
            else:
                pass

        self.setup_commands_stack.append(
            (reference, self.extract_setup_commands(data))
            )

    def pop_setup_commands(self, reference: str) -> list:
        """
        Pop setup commands from stack with same REFERENCE,
        if several setups commands blocks are founded, unify all into one
        """
        result = []

        # Get commands from stack with same reference
        for stack_reference, commands in self.setup_commands_stack:
            if stack_reference == reference:
                result += commands
                self.setup_commands_stack.remove((stack_reference, commands))

        return result

    def push_teardown_commands(self) -> None:
        """
        Push teardown commands to stack
        """
        debug.trace(7, 'parser.push_teardown_commands()')

        data = self.get_current_token().data

        self.eat(TokenType.TEARDOWN)
        ## TODO: rename extract_setup_commands to a common name
        commands = self.extract_setup_commands(data)

        self.teardown_commands_stack.append(commands)

    def pop_teardown_commands(self) -> None:
        """
        Pop teardown commands from stack
        """
        debug.trace(7, f'parser.pop_teardown_commands()')
        result = self.teardown_commands_stack
        self.teardown_commands_stack = []
        return result

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

    def build_assertion(self, reference:str='') -> None:
        """
        Build and append Assertion AST node and set REFERENCE as reference
        """
        debug.trace(7, f'parser.build_assertion(reference={reference})')
        assert reference, 'Invalid empty reference'

        data = self.get_current_token().data
        atype = None
        actual = ''

        # BAD:
        #   Do not use is_command_assertion_next or is_arrow_assertion_next here.
        #   because we need to check only the first token to ensure what assertion is next.

        # Check for command assertion
        ## TODO: move this to a different method (e.g. eat_command_assertion???)
        if self.get_current_token().type is TokenType.PESO:
            atype = AssertionType.OUTPUT
            self.eat(TokenType.PESO)
            actual = self.get_current_token().value
            self.eat(TokenType.TEXT)

        # Check for arrow assertion
        ## TODO: move this to a different method (e.g. eat_arrow_assertion???)
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
        ## TODO: move this to a different method
        expected = ''
        while self.get_current_token().type is TokenType.TEXT:
            expected += f'{self.get_current_token().value}\n'
            self.eat(TokenType.TEXT)
        expected = expected[:-1] # Remove last newline

        # New assertion node
        node = Assertion(
            atype=atype,
            setup_commands=self.pop_setup_commands(reference=reference),
            actual=actual,
            expected=expected,
            data=data,
            )

        self.assign_child_assertion_to_parent_test(node, reference)

    def assign_child_assertion_to_parent_test(
            self,
            assertion_node: Assertion,
            reference: str
            ) -> None:
        """
        Assign child assertion ast node into parent test ast node
        """
        for test in reversed(self.tests_ast_nodes_stack):
            if test.reference == reference:
                test.assertions.append(assertion_node)
                assertion_node = None
                break
        if assertion_node is not None:
            error(
                message=f'Assertion "{reference}" referenced before assignment.',
                text_line=assertion_node.data.text_line,
                line=assertion_node.data.line,
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
                self.push_test_ast_node()

            # Process next tokens as a continuation directive pattern
            #
            # Continuation pattern are brak
            # into Setup and Assertions nodes
            elif token_type is TokenType.CONTINUATION:
                self.break_continuation()

            # Process next tokens as a setup directive pattern
            elif token_type is TokenType.SETUP:
                self.push_setup_commands()

            # Process next tokens as teardown directive pattern
            elif token_type is TokenType.TEARDOWN:
                self.push_teardown_commands()

            # Create new test node for standlone commands and assertions
            elif self.is_command_next() or self.is_assertion_next():
                self.push_test_ast_node(f'test of line {current_token.data.line}')

            # (Only when embedded_tests!) skip standlone text tokens
            elif self.embedded_tests and token_type is TokenType.TEXT:
                self.eat(TokenType.TEXT)

            # Finish
            else:
                break

        # The last token always should be an EOF
        self.eat(TokenType.EOF)

        # Set global global setup for test suite
        setup_commands = self.pop_setup_commands(reference='')

        # Finishing the parsing, cannot be remaining setups on stack
        ## TODO: move this to a different class method (e.g. ensure_setup_stack_clean????).
        if self.setup_commands_stack:
            first_invalid = self.setup_commands_stack[0]
            error(
                message=f'Setup "{first_invalid.reference}" referenced before assignment.',
                text_line=first_invalid.data.text_line,
                line=first_invalid.data.line,
                column=None,
                )

        result = TestsSuite(
            self.pop_tests_ast_nodes(),
            setup_commands = setup_commands,
            teardown_commands = self.pop_teardown_commands(),
            )
        debug.trace(7, f'parser.build_tests_suite() => {result}')
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
