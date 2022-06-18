#!/usr/bin/env python3
#
# Interpreter module
#
# This module is responsible for interpret and build
# bats-core tests from Abstract Syntax Trees (AST) for Batspp
#
## TODO: debug - pretty print '='
## TODO: debug - bash debug print function to avoid repeated debug code
## TODO: debug - add pipe to "hexview.perl" to debug and submodule
## TODO: make setups commands output nothing
## TODO: some assertion commands (e.g. tee) that prints to stdout brokes the debug actual-expected text


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
from parser import AST, TestsSuite, Test, Setup, Assertion


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
        self.test_title = self.unspaced_test_title = ''

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

        result += '\n\n' if is_global_setup else ''

        debug.trace(7, f'interpreter.visit_Setup(node={node}) => {result}')
        return result

    def check_root(self, commands):
        """Check if command need root permissions"""
        if not self.root_required:
            self.root_required = 'sudo' in commands

    # pylint: disable=invalid-name
    def visit_Test(self, node: Test) -> str:
        """Visit Test node"""

        # Process title
        self.test_title = node.pointer
        self.unspaced_test_title = re.sub(r' +', '-', self.test_title.lower())

        # Test with default local setup
        result = (f'@test "{self.test_title}" {{\n'
                  f'\ttest_folder=$(echo /tmp/{self.unspaced_test_title}-$$)\n'
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
        """Visit Assertion node"""

        # Set actual and expected function names
        actual_function = f'{self.unspaced_test_title}-line{node.data.line}-actual'
        expected_function = f'{self.unspaced_test_title}-line{node.data.line}-expected'

        # Format setup nodes
        setup = self.visit(node.setup) if node.setup else ''

        # Format assertion
        result = (f'\n\t# Assertion of line {node.data.line}\n'
                  f'{setup}'
                  f'\tactual=$({actual_function})\n'
                  f'\texpected=$({expected_function})\n'
                  f'\techo "========== actual =========="\n'
                  f'\techo "$actual"\n'
                  f'\techo "========= expected ========="\n'
                  f'\techo "$expected"\n'
                  '\techo "============================"\n'
                  f'\t[ "$actual" == "$expected" ]\n')

        self.check_root(node.actual)

        # NOTE: we use functions to avoid sanitization poblems with '(' and ')'

        # Append actual function
        function = (f'function {actual_function} () {{\n'
                    f'\t{node.actual.strip()}\n'
                    '}\n\n')
        self.stack_functions.append(function)

        # Append expected function
        function = (f'function {expected_function} () {{\n'
                    f'\techo -e {repr(node.expected)}\n'
                    '}\n\n')
        self.stack_functions.append(function)

        debug.trace(7, f'interpreter.visit_Assertion(node={node}) => {result}')
        return result

    def interpret(self, tree: AST) -> str:
        """Interpret and visit bats-core tests"""

        self.root_required = False

        # Interpret
        assert tree, 'Invalid tree node'
        result = self.visit(tree)

        debug.trace(7, f'Interpreter.interpret() => root={self.root_required} result={result}')
        return self.root_required, result
