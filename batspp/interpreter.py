#!/usr/bin/env python3
#
# Interpreter module
#
# This module is responsible for interpret and build
# bats-core tests from Abstract Syntax Trees (AST) for Batspp
#
## TODO: make setups commands output nothing


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
from parser import (
    AST, TestsSuite, Test, Setup, Assertion, AssertionType
)


# Test file constants names
#
# NOTE: these can be diferent from the
#       Batspp command-line labels
VERBOSE_DEBUG = 'VERBOSE_DEBUG'


class TestData:
    """Data class for tests related data"""

    def __init__(self,
                 source: str = '',
                 embedded_tests:bool = False,
                 verbose_debug:bool = False) -> None:
        self.source = source
        self.embedded_tests = embedded_tests
        self.verbose_debug = verbose_debug


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

        # Test with default local setup
        result = (f'@test "{self.last_title}" {{\n'
                  f'\ttest_folder=$(echo /tmp/{self.get_unspaced_title()}-$$)\n'
                  f'\tmkdir $test_folder && cd $test_folder\n')

        # Visit assertions
        for assertion in node.assertions:
            result += self.visit(assertion)

        result += '}\n\n'

        # Append functions
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

        # Unify everything
        result = (f'\n\t# Assertion of line {node.data.line}\n'
                  f'{setup}'
                  f'\tactual=$({actual_function})\n'
                  f'\texpected=$({expected_function})\n'
                  '\tprint_debug "$actual" "$expected"\n'
                  f'\t[ "$actual" {operator} "$expected" ]\n')

        # Check global class flags to
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
        Return debug code,
        with HEXVIEW true, adds pipe to print 
        hewview of actual and expected values
        """

        result = ('# This prints debug data when an assertion fail\n'
                  '# $1 -> actual value\n'
                  '# $2 -> expected value\n'
                  'function print_debug() {\n'
                  '\techo "=======  actual  ======="\n'
                  f'\tbash -c "echo \"$1\" ${VERBOSE_DEBUG}"\n'
                  '\techo "======= expected ======="\n'
                  f'\tbash -c "echo \"$2\" ${VERBOSE_DEBUG}"\n'
                  '\techo "========================"\n'
                  '}\n\n')

        debug.trace(7,f'Interpreter.implement_debug() => {result}')
        return result

    def implement_constants(self, data: TestData):
        """Implement settings constants from DATA"""

        # This appends all constants that will be
        # used in the tests file, for example
        #
        # # Constants
        # VERBOSE_DEBUG="| hexview"
        # .
        # .
        # .
        # TEMP_DIR="/tmp"

        result, constants = '', ''

        if self.debug_required:
            ## TODO: implement hexview
            hexview = '' if data and data.verbose_debug else ''
            constants += f'{VERBOSE_DEBUG}="{hexview}"\n'

        # Add header comment
        result = f'# Constants\n{constants}\n' if constants else ''

        debug.trace(7, f'Interpreter.implement_constants() => "{result}"')
        return result

    def interpret(self,
                  tree: AST,
                  data: TestData = None) -> str:
        """
        Interpret Batspp abstract syntax tree and build tests
        """

        # Clean global class values
        #
        # This is useful if is needed to reuse
        # the same instance of this class
        self.stack_functions = []
        self.last_title = ''
        self.debug_required = False

        # Interpret abstract syntax tree tests
        assert tree, 'Invalid tree node'
        tests = self.visit(tree)

        # Add aditional content
        result = ''

        if tests:
            # Add tests header
            result += ('#!/usr/bin/env bats\n'
                       '#\n'
                       '# This test file was generated using Batspp\n'
                       '# https://github.com/LimaBD/batspp\n'
                       '#\n\n')

            result += self.implement_constants(data)

            if data and data.source:
                result += ('# Load sources\n'
                            'shopt -s expand_aliases\n'
                            f'source {data.source}\n')

            result += tests

            # Add implement debug
            result += self.implement_debug() if self.debug_required else ''

        debug.trace(7, f'Interpreter.interpret() => "{result}"')
        return result
