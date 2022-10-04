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
from re import sub as re_sub

# Installed packages
from mezcla import debug

# Local packages
from batspp.batspp_opts import BatsppOpts
from batspp.batspp_args import BatsppArgs
from batspp._ast_nodes import (
    TestsSuite, Test,
    Assertion, AssertionType,
    )
from batspp._exceptions import (
    warning_not_intended_for_cmd,
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
        # Global states variables
        self.opts = BatsppOpts()
        self.args = BatsppArgs()
        self.last_title = ''
        self.debug_required = False

    def reset_global_state_variables(self) -> None:
        """Reset global states variables"""
        self.__init__()

    # pylint: disable=invalid-name
    def visit_TestsSuite(self, node: TestsSuite) -> str:
        """Visit TestsSuite NODE"""

        result = ''

        # Global setups are formated into a function
        if node.tests:
            result += build_setup_function(
                commands = node.setup_commands,
                test_folder = True,
                copy_dir = self.args.copy_dir,
                )
            result += build_teardown_function(
                commands = node.teardown_commands,
                )

        # Visit tests nodes
        result += ''.join([self.visit(test) for test in node.tests])

        debug.trace(7, f'interpreter.visit_TestsSuite(node={node}) => {result}')
        return result

    # pylint: disable=invalid-name
    def visit_Test(self, node: Test) -> str:
        """
        Visit Test NODE, also updates global class test title
        """

        self.last_title = node.reference

        # Test header
        result = (
            f'@test "{self.last_title}" {{\n'
            f'\t{SETUP_FUNCTION} "{flatten_str(self.last_title)}"\n'
            )

        # Visit assertions
        result += ''.join([self.visit(asn) for asn in node.assertions])

        # Test footer
        result += (
            '\n'
            f'\t{TEARDOWN_FUNCTION}\n'
            '}\n\n'
            )

        debug.trace(7, f'interpreter.visit_Test(node={node}) => {result}')
        return result

    # pylint: disable=invalid-name
    def visit_Assertion(self, node: Assertion) -> str:
        """
        Visit Assertion NODE, also push functions
        to stack for actual and expected values
        """

        # Set setup
        setup = build_commands_block(node.setup_commands) if node.setup_commands else ''

        # Set assertion operator
        operator = ''
        if node.atype in [AssertionType.OUTPUT, AssertionType.EQUAL]:
            operator = '=='
        else:
            operator = '!='

        # Set debug
        debug_cmd = ''
        if not self.opts.omit_trace:
            debug_cmd = (
                f'\tprint_debug "$({node.actual.strip()})" "$(echo -e {repr(node.expected)})"\n'
                )

        # Unify everything
        result = (
            f'\n\t# Assertion of line {node.data.line}\n'
            f'{setup}'
            '\tshopt -s expand_aliases\n'
            f'{debug_cmd}'
            f'\t[ "$({node.actual.strip()})" {operator} "$(echo -e {repr(node.expected)})" ]\n'
            )

        # Check global class option to
        # later implement a debug function
        self.debug_required = True

        debug.trace(7, f'interpreter.visit_Assertion(node={node}) => {result}')
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

    def get_args_commands(self):
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
            commands += [f'source {src}' for src in self.args.sources]

        return commands

    def interpret(
            self,
            tree: TestsSuite,
            opts: BatsppOpts = BatsppOpts(),
            args: BatsppArgs = BatsppArgs(),
            ) -> str:
        """
        Interpret Batspp abstract syntax tree and build tests
        """

        assert tree, 'invalid tree node'

        self.reset_global_state_variables()
        self.opts = opts
        self.args = args

        # Append commands passed by arguments
        # (not in test file) to a setup global
        args_commands = self.get_args_commands()
        if args_commands:
            tree.setup_commands += args_commands

        # Visit abstract syntax tree nodes
        tests = self.visit(tree)

        # Add aditional content
        result = ''

        if tests:
            # Add tests header
            result += (
                '#!/usr/bin/env bats'
                f'{" " if self.args.run_opts else ""}'
                f'{self.args.run_opts}\n'
                '#\n'
                '# This test file was generated using Batspp\n'
                '# https://github.com/LimaBD/batspp\n'
                '#\n\n'
                )

            result += self.implement_constants()

            # Add tests
            result += tests

            # Add implement debug
            if self.debug_required and not self.opts.omit_trace:
                result += build_debug_function()

        debug.trace(7, f'Interpreter.interpret() => "{result}"')
        return result


def flatten_str(string: str) -> str:
    """Returns unspaced and lowercase STRING"""
    result = re_sub(r' +', '-', string.lower())
    debug.trace(7, f'interpreter.flatten_str({string}) => {result}')
    return result


def build_commands_block(
        commands: list,
        indent: str = '\t',
        ) -> str:
    """Build commands block with COMMANDS indented with tab"""
    result = ''.join([f'{indent}{cmd.strip()}\n' for cmd in commands])
    debug.trace(7, f'interpreter.build_commands_block({commands}) => {result}')
    return result


def build_setup_function(
        commands: list = None,
        test_folder: bool = True,
        copy_dir: bool = False,
        ) -> str:
    """
    Build setup function with
    default commands and specified COMMANDS
    """

    result = ''

    # Work-around to source files one time and
    # before create a default test folder
    sources = []
    for cmd in commands:
        if 'shopt -s expand_aliases' in cmd or 'source ' in cmd:
            sources.append(cmd)
    if sources:
        commands = list(set(sources) - set(commands))
        result += (
            '# One time global setup\n'
            f'{build_commands_block(sources, indent="")}'
            '\n'
            )

    result += (
        '# Setup function\n'
        '# $1 -> test name\n'
        f'function {SETUP_FUNCTION} () {{\n'
        )

    if test_folder:
        result += (
            f'\ttest_folder=$(echo ${TEMP_DIR}/$1-$$)\n'
            '\tmkdir --parents "$test_folder"\n'
            '\tcd "$test_folder" || echo Warning: Unable to "cd $test_folder"\n'
            )

    if copy_dir:
        # NOTE: warning added on 'cd "$test_folder"' for sake of shellcheck
        result += (
            '\tcommand cp $COPY_DIR "$test_folder"\n'
            )

    result += build_commands_block(commands)

    result += '}\n\n'

    debug.trace(7, f'interpreter.build_global_setup({commands}) => {result}')
    return result


def build_teardown_function(commands: list) -> str:
    """Build teardown function"""

    body = ''

    if commands:
        body = build_commands_block(commands)
    else:
        body = '\t: # Nothing here...\n'

    result = (
        '# Teardown function\n'
        f'function {TEARDOWN_FUNCTION} () {{\n'
        f'{body}'
        '}\n\n'
        )

    debug.trace(7, f'interpreter.build_teardown_function({commands}) => {result}')
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


if __name__ == '__main__':
    warning_not_intended_for_cmd()
