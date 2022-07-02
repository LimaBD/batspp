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

    def __init__(self) -> None:
        self.root_required = False
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

        self.check_root(result)

        result += '\n' if not self.last_title else ''

        debug.trace(7, f'interpreter.visit_Setup(node={node}) => {result}')
        return result

    def check_root(self, commands: str) -> None:
        """Check if COMMANDS need root permissions"""
        if not self.root_required:
            self.root_required = 'sudo' in commands

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
        # and return if root is needed
        self.debug_required = True
        self.check_root(node.actual)

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

    def implement_debug(self, hexview:bool=False) -> str:
        """
        Return debug code,
        with HEXVIEW true, adds pipe to print 
        hewview of actual and expected values
        """

        ## TODO: Implement hexview to print detailed debug data
        hexview = '' if hexview else ''

        result = ('# This prints debug data when an assertion fail\n'
                  '# $1 -> actual value\n'
                  '# $2 -> expected value\n'
                  'function print_debug() {\n'
                  '\techo "=======  actual  ======="\n'
                  f'\techo "$1"{hexview}\n'
                  '\techo "======= expected ======="\n'
                  f'\techo "$2"{hexview}\n'
                  '\techo "========================"\n'
                  '}\n\n')

        debug.trace(7,f'Interpreter.implement_debug(hexview={hexview}) => {result}')
        return result

    def interpret(self, tree: AST, debug_hexview:bool = False) -> str:
        """
        Interpret Batspp abstract syntax tree,
        if DEBUG_HEXVIEW is true, adds pipe to print hexview of actual and expected
        """

        # Clean global class values
        #
        # This is useful if is needed to reuse
        # the same instance of this class
        self.root_required = False
        self.stack_functions = []
        self.last_title = ''
        self.debug_required = False

        # Interpret
        assert tree, 'Invalid tree node'
        result = self.visit(tree)

        # Aditional
        result += self.implement_debug(debug_hexview) if self.debug_required else ''

        debug.trace(7, f'Interpreter.interpret() => root={self.root_required} result={result}')
        return self.root_required, result
