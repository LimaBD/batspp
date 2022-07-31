#!/usr/bin/env python3
#
# Interpreter module
#
# This module is responsible for interpret and build
# bats-core tests from Abstract Syntax Trees (AST) for Batspp
#
## TODO: make setups commands output nothing
## TODO: implement setup and teardown bats functions


"""
Interpreter module

This module is responsible for interpret and build
bats-core tests from abstract syntax trees for Batspp
"""


# Standard packages
import re


# Installed packages
from mezcla import debug


# Local modules
from batspp_opts import BatsppOpts
from batspp_args import BatsppArgs
from parser import (
    TestsSuite, Test, Setup,
    Assertion, AssertionType
)


# Test file constants names
#
# NOTE: these can be diferent from the
#       Batspp command-line labels
VERBOSE_DEBUG = 'VERBOSE_DEBUG'
TEMP_DIR = 'TEMP_DIR'
COPY_DIR = 'COPY_DIR'


class NodeVisitor:
    """Implements a generic method visit"""

    def visit(self, node):
        """Generic method to visit NODE"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visitor)
        debug.trace(7, f'NodeVisitor.visitor({node}) => {method_name}({node})')
        return visitor(node)

    def generic_visitor(self, node) -> None:
        """Raise exception if the visit method to NODE not exist"""
        raise Exception(f'No visit_{type(node).__name__} method founded')


class Interpreter(NodeVisitor):
    """
    This is responsible for interpret and builds
    bats-core tests from abstract syntax trees for Batspp
    """
    ## TODO: this bad smells, inteprets an AST and
    ##       also builds a full tests content.

    def __init__(self) -> None:
        # Test related options and constants
        self.opts = BatsppOpts()
        self.args = BatsppArgs()

        # Global state
        self.stack_functions = []
        self.last_title = ''
        self.debug_required = False

    def get_unspaced_title(self) -> str:
        """Get unspaced title"""
        return re.sub(r' +', '-', self.last_title.lower())

    # pylint: disable=invalid-name
    def visit_TestsSuite(self, node: TestsSuite) -> str:
        """Visit TestsSuite NODE"""

        result = ''

        # Visit (global) setup node
        result += self.visit(node.setup) if node.setup else ''

        # Visit tests nodes
        for test in node.tests:
            result += self.visit(test)

        debug.trace(7, f'interpreter.visit_TestsSuite(node={node}) => {result}')
        return result

    # pylint: disable=invalid-name
    def visit_Setup(self, node: Setup) -> str:
        """Visit Setup NODE"""

        # Check header comment and commands indentation
        result = '# Setup\n' if not self.last_title else ''
        indent = '\t' if self.last_title else ''

        # Append commands
        for command in node.commands:
            result += f'{indent}{command.strip()}\n'

        result += '\n' if not self.last_title else ''

        debug.trace(7, f'interpreter.visit_Setup(node={node}) => {result}')
        return result

    # pylint: disable=invalid-name
    def visit_Test(self, node: Test) -> str:
        """
        Visit Test NODE, also updates global class test title
        """

        # Process title
        self.last_title = node.pointer

        copy_cmd = f'\tcommand cp $COPY_DIR "$test_folder"\n' if self.args.copy_dir else ''

        # Test with default local setup
        # NOTE: warning added on 'cd "$test_folder"' for sake of shellcheck
        result = (f'@test "{self.last_title}" {{\n'
                  f'\ttest_folder=$(echo ${TEMP_DIR}/{self.get_unspaced_title()}-$$)\n'
                  '\tmkdir --parents "$test_folder"\n'
                  f'{copy_cmd}'
                  '\tcd "$test_folder" || echo Warning: Unable to "cd $test_folder"\n')

        # Visit assertions
        for assertion in node.assertions:
            result += self.visit(assertion)

        result += '}\n\n'

        # Pop functions from stack
        for function in self.stack_functions:
            result += function
        self.stack_functions = []

        debug.trace(7, f'interpreter.visit_Test(node={node}) => {result}')
        return result

    # pylint: disable=invalid-name
    def visit_Assertion(self, node: Assertion) -> str:
        """
        Visit Assertion NODE, also push functions
        to stack for actual and expected values
        """

        # Set function names for
        # actual and expected values
        actual_function = f'{self.get_unspaced_title()}-line{node.data.line}-actual'
        expected_function = f'{self.get_unspaced_title()}-line{node.data.line}-expected'

        # Visit setup nodes
        setup = self.visit(node.setup) if node.setup else ''

        # Set assertion operator
        operator = '==' if node.atype in [AssertionType.OUTPUT, AssertionType.EQUAL] else '!='

        # Set debug
        debug_cmd = f'\tprint_debug "$({actual_function})" "$({expected_function})"\n' if not self.opts.omit_trace else ''

        # Unify everything
        result = (f'\n\t# Assertion of line {node.data.line}\n'
                  f'{setup}'
                  f'{debug_cmd}'
                  f'\t[ "$({actual_function})" {operator} "$({expected_function})" ]\n')

        # Check global class option to
        # later implement a debug function
        self.debug_required = True

        # NOTE: we use functions to avoid sanitization
        #       poblems with '(' and ')'

        # Push to stack function for the actual value
        function = (f'function {actual_function} () {{\n'
                    f'\t{node.actual.strip()}\n'
                    '}\n\n')
        self.stack_functions.append(function)

        # Push to stack function for the expected value
        function = (f'function {expected_function} () {{\n'
                    f'\techo -e {repr(node.expected)}\n'
                    '}\n\n')
        self.stack_functions.append(function)

        debug.trace(7, f'interpreter.visit_Assertion(node={node}) => {result}')
        return result

    def implement_debug(self) -> str:
        """
        Return debug code
        """

        result = ('# This prints debug data when an assertion fail\n'
                  '# $1 -> actual value\n'
                  '# $2 -> expected value\n'
                  'function print_debug() {\n'
                  '\techo "=======  actual  ======="\n'
                  f'\tbash -c "echo \\\"$1\\\" ${VERBOSE_DEBUG}"\n'
                  '\techo "======= expected ======="\n'
                  f'\tbash -c "echo \\\"$2\\\" ${VERBOSE_DEBUG}"\n'
                  '\techo "========================"\n'
                  '}\n\n')

        debug.trace(7,f'Interpreter.implement_debug() => {result}')
        return result

    def implement_constants(self):
        """Implement test constants from arguments"""

        # This appends all constants that will be
        # used in the tests file, for example
        #
        # # Constants
        # VERBOSE_DEBUG="| hexdump -C"
        # .
        # .
        # .
        # TEMP_DIR="/tmp"

        result, constants = '', ''

        # Append default VERBOSE_DEBUG constant
        #
        # NOTE: BatsppOpts.verbose_debug are used to
        #       default debug, for now is equivalent to hexdump_debug.
        if self.debug_required:
            value = ''
            if self.args.debug:
                value = self.args.debug
            elif self.opts.verbose_debug or self.opts.hexdump_debug:
                # More information about hexdump command:
                # - https://linoxide.com/linux-hexdump-command-examples/
                value = '| hexdump -C'
            constants += f'{VERBOSE_DEBUG}="{value}"\n'

        # Append TEMP_DIR constant
        value = self.args.temp_dir if self.args.temp_dir else '/tmp'
        constants += f'{TEMP_DIR}="{value}"\n'

        # Append COPY_DIR constant
        constants += f'{COPY_DIR}="{self.args.copy_dir}"\n' if self.args.copy_dir else ''

        # Add header comment
        result = f'# Constants\n{constants}\n' if constants else ''

        debug.trace(7, f'Interpreter.implement_constants() => "{result}"')
        return result

    def commands_from_args(self):
        """
        Return a list of aditional setup commands from arguments
        """
        commands = []

        # Check for visible path argument
        if self.args.visible_paths:
            commands.append(f'PATH={":".join(self.args.visible_paths)}:$PATH\n')

        # Check for sources files
        if (self.args.sources and
            not self.opts.disable_aliases):
            source_commands = [f'source {src}' for src in self.args.sources]
            if source_commands:
                commands.append('shopt -s expand_aliases\n')
                commands += source_commands

        return commands

    def interpret(self,
                  tree: TestsSuite,
                  opts: BatsppOpts = BatsppOpts(),
                  args: BatsppArgs = BatsppArgs()) -> str:
        """
        Interpret Batspp abstract syntax tree and build tests
        """

        assert tree, 'invalid tree node'

        # Clean global class values
        #
        # This is useful if is needed to reuse
        # the same instance of this class
        self.opts = opts
        self.args = args
        self.stack_functions = []
        self.last_title = ''
        self.debug_required = False

        # Append commands passed by arguments
        # (not in test file) to a setup global
        aditional_commands = self.commands_from_args()
        if aditional_commands:
            if tree.setup:
                tree.setup.commands += aditional_commands
            else:
                tree.setup = Setup(commands=aditional_commands)

        # Visit abstract syntax tree nodes
        tests = self.visit(tree)

        # Add aditional content
        result = ''

        if tests:
            # Add tests header
            result += (f'#!/usr/bin/env bats'
                       f'{" " if self.args.run_opts else ""}'
                       f'{self.args.run_opts}\n'
                       '#\n'
                       '# This test file was generated using Batspp\n'
                       '# https://github.com/LimaBD/batspp\n'
                       '#\n\n')

            result += self.implement_constants()

            # Add tests
            result += tests

            # Add implement debug
            result += self.implement_debug() if self.debug_required and not self.opts.omit_trace else ''

        debug.trace(7, f'Interpreter.interpret() => "{result}"')
        return result
