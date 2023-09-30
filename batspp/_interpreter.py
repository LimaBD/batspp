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
    ASSERT_EQ, ASSERT_NE,
    )    

# Constants
#
# Note that some constants related to the Batspp
# command-line argument processing class can vary,
# these constants arent duplicated.
VERBOSE_DEBUG = 'VERBOSE_DEBUG'
TEMP_DIR = 'TEMP_DIR'
COPY_DIR = 'COPY_DIR'
SETUP_FUNCTION = 'run_setup'
TEARDOWN_FUNCTION = 'run_teardown'

class Interpreter(ReferenceNodeVisitor):
    """
    This is responsible for interpret and builds
    bats-core tests from abstract syntax trees for Batspp
    """

    def __init__(self) -> None:
        # Global states variables
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
            '#!/usr/bin/env bats'
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
        debug_function_text = ''
        if self.opts.verbose_debug and not self.opts.omit_trace:
            debug_function_text += build_debug_function()
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
                + debug_function_text \
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
        result += build_commands_block(self.visit(node.commands), '\t')
        result += '' if result.endswith('\n') else '\n'
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
            body = '\t: # Nothing here...'
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
        name = self.visit(node.reference)
        # Test header
        # with call to a global setup function
        result = (
            f'@test "{name}" {{\n'
            f'\t{SETUP_FUNCTION} "{flatten_str(name)}"\n'
            )
        # Visit assertions
        # Note that due to the semantic analyzer,
        # only tests should be here
        for t in node.setup_assertions:
            assert isinstance(t, SetupAssertion), 'Only SetupAssertion nodes should be at this point'
            result += self.visit(t)
        # Test footer
        # with call to a global teardown function
        result += (
            '\n'
            f'\t{TEARDOWN_FUNCTION}\n'
            '}\n\n'
            )
        debug.trace(7, f'interpreter.visit_Test(node={node}) => {result}')
        return result

    # pylint: disable=invalid-name
    def visit_Setup(self, node: Setup) -> str:
        """
        Visit Setup NODE
        """
        result = self.visit(node.commands)
        if result and not result.endswith('\n'):
            result += '\n'
        return result

    # pylint: disable=invalid-name
    def visit_StandaloneCommands(self, node:StandaloneCommands) -> str:
        """
        Visit StandaloneCommands NODE
        """
        result = ''
        cmds = [ self.visit(cmd) for cmd in node.commands ]
        result += build_commands_block(cmds)
        result += '\n' if result and not result.endswith('\n') else ''
        return result

    # pylint: disable=invalid-name
    def visit_SetupAssertion(self, node: SetupAssertion) -> str:
        """
        Visit SetupAssertion NODE
        """
        result = (
            f'\n\t# Assertion of line {node.assertion.line}\n'
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
            result += '\n'.join([ self.visit(ext) for ext in node.extensions ])
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
        actual = actual.strip().rstrip('\n')
        expected = repr(expected.strip().rstrip('\n') + '\n')
        # Set debug
        debug_cmd = ''
        if not self.opts.omit_trace:
            debug_cmd = (
                '\tshopt -s expand_aliases\n'
                f'\tprint_debug "$({actual})" "$(echo -e {expected})"\n'
                )
        # Unify everything
        result = (
            f'{debug_cmd}'
            f'\t[ "$({actual})" {operator} "$(echo -e {expected})" ]\n'
            )
        debug.trace(7, f'interpreter.build_assertion(operator={operator}, actual={actual}, expeted={expected}) => {result}')
        return result

    def visit_MultilineText(self, node: MultilineText) -> str:
        """
        Visit MultilineText NODE
        """
        result = ''
        for txt in node.text_lines:
            if txt:
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
        assert tree, 'invalid tree node'
        #
        self.reset_global_state_variables()
        self.opts = opts
        self.args = args
        #
        tests = self.visit(tree)
        debug.trace(7, f'Interpreter.interpret() => "{tests}"')
        return tests

def flatten_str(string: str) -> str:
    """Returns unspaced and lowercase STRING"""
    result = re_sub(r' +', '-', string.lower())
    debug.trace(7, f'interpreter.flatten_str({string}) => {result}')
    return result

def build_commands_block(
        commands: list,
        indent: str = '\t',
        multiline_last_char: str = '\n',
        ) -> str:
    """Build commands block with COMMANDS indented with tab"""
    if isinstance(commands, str):
        commands = commands.split('\n')
    commands = [ cmd for cmd in commands if cmd and cmd != '\n' ]
    multiline_last_char = multiline_last_char if len(commands) > 1 else ''
    result = ''.join([f'{indent}{cmd.strip()}{multiline_last_char}' for cmd in commands])
    debug.trace(7, f'interpreter.build_commands_block({commands}) => {result}')
    return result

def build_debug_function() -> str:
    """Build debug function"""
    # NOTE: this provide a debug trace too.

    result = (
        '# This prints debug data when an assertion fail\n'
        '# $1 -> actual value\n'
        '# $2 -> expected value\n'
        'function print_debug() {\n'
        '\techo "=======  actual  ======="\n'
        f'\tbash -c "echo \\\"$1\\\" ${VERBOSE_DEBUG}"\n'
        '\techo "======= expected ======="\n'
        f'\tbash -c "echo \\\"$2\\\" ${VERBOSE_DEBUG}"\n'
        '\techo "========================"\n'
        '}\n\n'
        )

    debug.trace(7, 'interpreter.build_debug()')
    return result

interpreter = Interpreter()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
