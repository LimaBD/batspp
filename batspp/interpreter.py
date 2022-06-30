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
        """Generic method to visit nodes"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visitor)
        debug.trace(7, f'NodeVisitor.visitor({node}) => {method_name}({node})')
        return visitor(node)

    def generic_visitor(self, node):
        """Raise exception if the visit method not exist"""
        raise Exception(f'No visit_{type(node).__name__} method founded')


class Interpreter(NodeVisitor):
    """
    This is responsible for interpret and builds
    bats-core tests from abstract syntax trees for Batspp
    """

    def __init__(self):
        self.root_required = False
        self.stack_functions = []
        self.last_title = ''
        self.implemented_debug = False

    def get_unspaced_title(self):
        """Get unspaced title"""
        return re.sub(r' +', '-', self.last_title.lower())

    # pylint: disable=invalid-name
    def visit_TestsSuite(self, node: TestsSuite) -> str:
        """Visit TestsSuite node"""

        result = ''

        # Interpret global setup node
        result += '' if node.setup is None else self.visit(node.setup)

        # Process tests nodes
        for test in node.tests:
            result += self.visit(test)

        debug.trace(7, f'interpreter.visit_TestsSuite(node={node}) => {result}')
        return result

    # pylint: disable=invalid-name
    def visit_Setup(self, node: Setup) -> str:
        """Visit Setup node"""

        is_global_setup = node.pointer in ['', None]

        # Check indentation and header
        result = '# Setup\n' if is_global_setup else ''
        indent = '\t' if not is_global_setup else ''

        # Append commands
        for command in node.commands:
            result += f'{indent}{command.strip()}\n'

        self.check_root(result)

        result += '\n' if is_global_setup else ''

        debug.trace(7, f'interpreter.visit_Setup(node={node}) => {result}')
        return result

    def check_root(self, commands):
        """Check if command need root permissions"""
        if not self.root_required:
            self.root_required = 'sudo' in commands

    # pylint: disable=invalid-name
    def visit_Test(self, node: Test) -> str:
        """
        Visit Test node, updates global class test title
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
        Visit Assertion node, also push functions
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
        self.implemented_debug = True
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

    def implement_debug(self, verbose:bool=False):
        """Return debug code"""

        ## TODO: Implement hexview to print detailed debug data
        hexview = '' if verbose else ''

        result = ('# This prints debug data when an assertion fail\n'
                  '# $1 -> actual value\n'
                  '# $2 -> expected value\n'
                  'function print_debug() {\n'
                  '\techo "=======  actual  ======="\n'
                  f'\techo "$1"{hexview}\n'
                  '\techo "======= expected ======="\n'
                  f'\techo "$2"{hexview}\n'
                  '\techo "============================"\n'
                  '}\n\n')

        debug.trace(7,f'Interpreter.implement_debug(verbose={verbose}) => {result}')
        return result

    def interpret(self, tree: AST, verbose:bool = False) -> str:
        """Interpret and visit bats-core tests"""

        # Clean global class values
        self.root_required = False
        self.stack_functions = []
        self.last_title = ''
        self.implemented_debug = False

        # Interpret
        assert tree, 'Invalid tree node'
        result = self.visit(tree)

        # Aditional
        result += self.implement_debug(verbose) if self.implemented_debug else ''

        debug.trace(7, f'Interpreter.interpret() => root={self.root_required} result={result}')
        return self.root_required, result
