#!/usr/bin/env python3
#
# Interpreter module
#
# This module is responsible for interpret and build
# bats-core tests from Abstract Syntax Trees (AST) for Batspp
#

"""
Interpreter module

This module is responsible for interpret and build
bats-core tests from abstract syntax trees for Batspp
"""

# Standard packages
from re import sub as re_sub

# Installed packages
from mezcla import debug

# Local packages
from batspp._node_visitor import (
    ReferenceNodeVisitor,
    )
from batspp.batspp_opts import BatsppOpts
from batspp.batspp_args import BatsppArgs
from batspp._ast_node import (
    TestSuite, TestOrSetup, GlobalTeardown,
    GlobalSetup, Setup, Test, CommandAssertion,
    Assertion, Command, MultilineText, Text,
    ArrowAssertion, StandaloneCommands, Constants,
    SetupAssertion, CommandExtension,
    )
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )
from batspp._token import (
    ASSERT_EQ, ASSERT_NE, Token
    )
from batspp._timer import Timer
from batspp._settings import (
    SETUP_FUNCTION, TEARDOWN_FUNCTION,
    )

# Constants
#
# Note that some constants related to the Batspp
# command-line argument processing class can vary,
# these constants arent duplicated.
VERBOSE_DEBUG = 'VERBOSE_DEBUG'
TEMP_DIR = 'TEMP_DIR'
COPY_DIR = 'COPY_DIR'

class Interpreter(ReferenceNodeVisitor):
    """
    This is responsible for interpret and builds
    bats-core tests from abstract syntax trees for Batspp
    """

    def __init__(self) -> None:
        """Initialize Interpreter class"""
        # Default options
        self.opts = BatsppOpts()
        self.args = BatsppArgs()

    def reset_global_state_variables(self) -> None:
        """Reset global states variables"""
        self.__init__()

    # pylint: disable=invalid-name
    def visit_TestSuite(self, node: TestSuite) -> str:
        """Visit TestSuite NODE"""
        # Build text parts
        header_text = (
            f'#!/usr/bin {self.args.runner}'
            f'{" " if self.args.run_opts else ""}'
            f'{self.args.run_opts}\n'
            '#\n'
            '# This test file was generated using Batspp\n'
            '# https://github.com/LimaBD/batspp\n'
            '#\n\n'
            )
        constants_text = self.visit(node.constants)
        global_setup_text = self.visit_optional(node.global_setup, '')
        global_teardown_text = self.visit_optional(node.global_teardown, '')
        # Tests suite should contain only tests on this point
        # due to the semantic analyzer that merges setups into tests
        tests_text = ''.join([self.visit(test) for test in node.tests_or_setups])
        # Finally merge all parts
        result = ''
        if tests_text:
            result += '' \
                + header_text \
                + constants_text \
                + global_setup_text \
                + global_teardown_text \
                + tests_text \
                + ''
        debug.trace(7, f'interpreter.visit_TestsSuite(node={node}) => {result}')
        return result

    # pylint: disable=invalid-name
    def visit_GlobalSetup(self, node: GlobalSetup) -> str:
        """
        Visit GlobalSetup NODE
        """
        result = ''
        if node.one_time_commands:
            commands = build_commands_block(self.visit(node.one_time_commands), "")
            if commands:
                result += (
                    '# One time global setup\n'
                    f'{commands}\n'
                    )
        result += (
            '# Setup function\n'
            '# $1 -> test name\n'
            f'function {SETUP_FUNCTION} () {{\n'
            )
        result += build_commands_block(self.visit(node.commands), '    ')
        result += '}\n\n'
        debug.trace(7, f'interpreter.visit_GlobalSetup() => {result}')
        return result

    # pylint: disable=invalid-name
    def visit_GlobalTeardown(self, node: GlobalTeardown) -> str:
        """
        Visit GlobalTeardown NODE
        """
        commands = []
        if node.commands:
            commands = self.visit(node.commands).split('\n')
        commands = [ cmd for cmd in commands if cmd and cmd != '\n' ]
        body = ''
        if commands:
            body = build_commands_block(commands)
        else:
            body = '    : # Nothing here...'
        result = (
            '# Teardown function\n'
            f'function {TEARDOWN_FUNCTION} () {{\n'
            f'{body}\n'
            '}\n\n'
            )
        debug.trace(7, f'interpreter.visit_GlobalTeardown() => {result}')
        return result

    # pylint: disable=invalid-name
    def visit_TestOrSetup(self, node: TestOrSetup) -> str:
        """
        Visit Test NODE
        """
        return self.visit(node.child)

    # pylint: disable=invalid-name
    def visit_Test(self, node: Test) -> str:
        """
        Visit Test NODE, also updates global class test title
        """
        raise Exception('visit_Test must be implemented by subclasses')

    # pylint: disable=invalid-name
    def visit_Setup(self, node: Setup) -> str:
        """
        Visit Setup NODE
        """
        result = self.visit(node.commands)
        return result

    # pylint: disable=invalid-name
    def visit_StandaloneCommands(self, node:StandaloneCommands) -> str:
        """
        Visit StandaloneCommands NODE
        """
        result = ''
        cmds = [ self.visit(cmd) for cmd in node.commands ]
        result += build_commands_block(cmds)
        return result

    # pylint: disable=invalid-name
    def visit_SetupAssertion(self, node: SetupAssertion) -> str:
        """
        Visit SetupAssertion NODE
        """
        result = (
            f'\n    # Assertion of line {node.assertion.line}\n'
        )
        result += self.visit_optional(node.setup, '')
        result += self.visit(node.assertion)
        return result

    # pylint: disable=invalid-name
    def visit_Assertion(self, node: Assertion) -> str:
        """
        Visit Assertion NODE, also push functions
        to stack for actual and expected values
        """
        return self.visit(node.assertion)

    # pylint: disable=invalid-name
    def visit_CommandAssertion(self, node: CommandAssertion) -> str:
        """
        Visit CommandAssertion NODE
        """
        operator = '=='
        actual_commands = self.visit(node.command)
        expected_text = self.visit(node.expected)
        return self.build_assertion(
            operator,
            actual_commands,
            expected_text
            )

    # pylint: disable=invalid-name
    def visit_Command(self, node: Command) -> str:
        """
        Visit Command NODE
        """
        result = node.command.value
        if node.extensions:
            result += '\n' + '\n'.join([ self.visit(ext) for ext in node.extensions ])
        return result

    # pylint: disable=invalid-name
    def visit_CommandExtension(self, node: CommandExtension) -> str:
        """
        Visit CommandExtension NODE
        """
        return node.command.value

    # pylint: disable=invalid-name
    def visit_ArrowAssertion(self, node: ArrowAssertion) -> str:
        """
        Visit ArrowAssertion NODE
        """
        expected_text = self.visit(node.expected_lines)
        operator = None
        if node.assertion.variant is ASSERT_EQ:
            operator = '=='
        elif node.assertion.variant is ASSERT_NE:
            operator = '!='
        else:
            raise Exception(f'invalid assertion variant {node.assertion.variant}')
        return self.build_assertion(
            operator,
            node.actual.value,
            expected_text
            )

    def build_assertion(
            self,
            operator:str,
            actual:str,
            expected:str,
            ) -> str:
        """
        Build assertion
        """
        raise Exception('build_assertion must be implemented by subclasses')

    def visit_MultilineText(self, node: MultilineText) -> str:
        """
        Visit MultilineText NODE
        """
        result = ''
        for txt in node.text_lines:
            if isinstance(txt, Token):
                result += f'{txt.value}\n'
            else:
                result += f'{self.visit(txt)}\n'
        result += '' if result.endswith('\n') else '\n'
        return result

    # pylint: disable=invalid-name
    def visit_Constants(self, node: Constants) -> str:
        """Visit Constants NODE"""
        result = f'# Constants\n'
        result += '\n'.join([self.visit(cst) for cst in node.constants ])
        result += '\n\n'
        debug.trace(7, f'Interpreter.visit_Constants() => "{result}"')
        return result

    # pylint: disable=invalid-name
    def visit_Text(self, node: Text) -> str:
        """Visit Text NODE"""
        return node.text.value

    def interpret(
            self,
            tree: TestSuite,
            opts: BatsppOpts = BatsppOpts(),
            args: BatsppArgs = BatsppArgs(),
            ) -> str:
        """
        Interpret Batspp abstract syntax tree and build tests
        """
        timer = Timer()
        timer.start()
        assert tree, 'invalid tree node'
        #
        self.reset_global_state_variables()
        self.opts = opts
        self.args = args
        #
        tests = self.visit(tree)
        debug.trace(7, f'Interpreter.interpret() => "{tests}" in {timer.stop()} seconds')
        return tests

def flatten_str(string: str) -> str:
    """Returns unspaced and lowercase STRING"""
    result = re_sub(r' +', '-', string.lower())
    debug.trace(7, f'interpreter.flatten_str({string}) => {result}')
    return result

def build_commands_block(
        commands: list,
        indent: str = '    ',
        end_of_line: str = '\n',
        ) -> str:
    """Build commands block with COMMANDS indented with tab"""
    # Plit every line
    if isinstance(commands, str):
        commands = commands.split('\n')
    separated_commands = []
    for command in commands:
        separated_commands += command.split('\n')
    commands = separated_commands
    # Transform lines
    result = ''
    for command in commands:
        if not command or command == '\n':
            continue
        result += f'{indent}{command.strip()}{end_of_line}'
    if result and not result.endswith('\n'):
        result += '\n'
    debug.trace(7, f'interpreter.build_commands_block({commands}) => {result}')
    return result

if __name__ == '__main__':
    warning_not_intended_for_cmd()
