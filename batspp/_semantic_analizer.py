#!/usr/bin/env python3
#
# Semantic Analizer module
#
# This is responsible for the semantic analisis of the AST tree,
# this verify and modity the AST tree if necessary.

"""
Semantic Analizer module

This is responsible for the semantic analisis of the AST tree,
this verify and modity the AST tree if necessary.
"""

# Standard packages
## NOTE: this is empty for now

# Installed packages
from mezcla import debug

# Local packages
from batspp._exceptions import (
    warning_not_intended_for_cmd, error,
    )
from batspp._ast_node import (
    ASTnode, Setup, Test,
    GlobalTeardown, GlobalSetup,
    TestOrSetup, TestSuite,
    Constants, Text, Command,
    TestReference, ContinuationReferencePrefix,
    StandaloneCommands,
    )
from batspp._node_visitor import (
    ReferenceNodeVisitor,
    )
from batspp.batspp_args import (
    BatsppArgs,
    )
from batspp.batspp_opts import (
    BatsppOpts,
    )
from batspp._token import (
    Token, TEXT,
    )
from batspp._timer import Timer

# Constants
#
# Note that some constants related to the Batspp
# command-line argument processing class can vary,
# these constants arent duplicated.
VERBOSE_DEBUG = 'VERBOSE_DEBUG'
TEMP_DIR = 'TEMP_DIR'
COPY_DIR = 'COPY_DIR'

def build_command_node(command:str) -> Command:
    """Build a command node"""
    return Command(None, Token(TEXT, command), None)

def build_text_node(text:str) -> Text:
    """Build a text node"""
    return Text(Token(TEXT, text))

def build_test_reference(reference:str) -> TestReference:
    """Build a test reference node"""
    return TestReference(None, Token(TEXT, reference))

def build_setup_node(commands:list) -> Setup:
    """Build a setup node"""
    return Setup(
        reference=None,
        commands=StandaloneCommands(commands),
        )

class Entity:
    """Semantic entity class"""

    def __init__(self, reference:str, node:ASTnode) -> None:
        """Initialize the class"""
        self.reference = reference
        self.node = node

class _SemanticAnalizer(ReferenceNodeVisitor):
    """Semantic analizer class"""

    def __init__(self) -> None:
        """Initialize the class"""
        self._entities = []
        self.args = BatsppArgs()
        self.opts = BatsppOpts()

    def _append_entity(self, reference:str, node: ASTnode) -> None:
        """Append NODE with REFERENCE to the list of entities"""
        self._entities.append(Entity(reference, node))

    # pylint: disable=invalid-name
    def visit_Setup(self, node: Setup) -> None:
        """Visit a Setup node"""
        reference = self.visit(node.reference)
        if self.is_referenced_before_assignment(reference):
            error(
                message=f'Setup "{reference}" referenced before assignment.',
                )
        self._append_entity(reference, node)

    # pylint: disable=invalid-name
    def visit_Test(self, node: Test) -> None:
        """Visit a Test node"""
        reference = ''
        # Check for reference
        if node.reference is None:
            reference = f'test of line {node.line}'
            node.reference = build_test_reference(reference)
        else:
            reference = self.visit(node.reference)
            is_continuation = not isinstance(node.reference.pointer, Token)
            if is_continuation and self.is_referenced_before_assignment(reference):
                error(
                    message=f'Continuation "{reference}" referenced before assignment.',
                    )
        self._append_entity(reference, node)
        # Enable debug if test is present
        self.opts.verbose_debug = True

    # pylint: disable=invalid-name
    def visit_GlobalTeardown(self, node: GlobalTeardown) -> None:
        """Visit a GlobalTeardown node"""
        # Nothing

    # pylint: disable=invalid-name
    def visit_GlobalSetup(self, node: GlobalSetup) -> None:
        """Visit a GlobalSetup node, verify and insert commands"""
        one_time_setup_commands = []
        setup_commands = []

        # Add commands to visible paths
        if self.args.visible_paths:
            value = f'PATH={":".join(self.args.visible_paths)}:$PATH\n'
            one_time_setup_commands.append(build_command_node(value))

        # Add source commands
        if (self.args.sources and
            not self.opts.disable_aliases):
            one_time_setup_commands.append(build_command_node('shopt -s expand_aliases'))
            for source in self.args.sources:
                one_time_setup_commands.append(build_command_node(f'source {source}\n'))

        # Add default commands to global setup node
        # NOTE: warning added on 'cd "$test_folder"' for sake of shellcheck
        default_commands = [
            f'test_folder=$(echo ${TEMP_DIR}/$1-$$)',
            'mkdir --parents "$test_folder"',
            'cd "$test_folder" || echo Warning: Unable to "cd $test_folder"',
        ]
        if self.args.copy_dir:
            default_commands.append('command cp $COPY_DIR "$test_folder"')
        for command in default_commands:
            setup_commands.append(build_command_node(command))

        # Work-around to source files one time and
        # before create a default test folder
        target_commands = [
            'shopt -s expand_aliases',
            'source ',
            ]
        for cmd in node.commands.commands:
            assert isinstance(cmd, Command), 'Command node expected'
            # Check in all command-extension values
            values = [ cmd.command.value ]
            values += [ cmd.command.value for cmd in cmd.extensions ]
            for val in values:
                if val.lstrip().startswith(tuple(target_commands)):
                    one_time_setup_commands.append(cmd)
                else:
                    setup_commands.append(cmd)

        node.one_time_commands.commands = one_time_setup_commands
        node.commands.commands = setup_commands

    # pylint: disable=invalid-name
    def visit_TestOrSetup(self, node: TestOrSetup) -> None:
        """Visit a TestOrSetup node"""
        self.visit(node.child)

    # pylint: disable=invalid-name
    def visit_TestSuite(self, node: TestSuite) -> None:
        """Visit a TestSuite node"""
        node.constants = self.build_constants_node()
        #
        if not node.global_setup:
            node.global_setup = GlobalSetup(None, StandaloneCommands([]))
        self.visit(node.global_setup)
        #
        if not node.global_teardown:
            node.global_teardown = GlobalTeardown(None, StandaloneCommands([]))
        self.visit(node.global_teardown)
        #
        for test_or_setup in node.tests_or_setups:
            self.visit(test_or_setup)
        #
        node.tests_or_setups = self.merged_entities_into_tests()

    def merged_entities_into_tests(self) -> list:
        """Return list of tests with merged setups and continuations"""
        tests = []
        setup_stack = []
        for entity in self._entities:
            if isinstance(entity.node, Setup):
                setup_stack.append(entity)
            elif isinstance(entity.node, Test):
                # Merge setups into next test node, only if
                # has the same reference or is unreferenced.
                commands_to_merge = []
                new_setup_stack = []
                for setup in setup_stack:
                    no_reference = setup.reference is None or setup.reference == ''
                    same_reference = setup.reference == entity.reference
                    if no_reference or same_reference:
                        commands_to_merge += setup.node.commands.commands
                    else:
                        new_setup_stack.append(setup)
                setup_stack = new_setup_stack
                # Add found setups to the first assertion
                if not entity.node.setup_assertions[0].setup:
                    entity.node.setup_assertions[0].setup = build_setup_node(commands_to_merge)
                else:
                    entity.node.setup_assertions[0].setup.commands.commands = [] \
                        + commands_to_merge \
                        + entity.node.setup_assertions[0].setup.commands.commands
                # Merge continuation tests into a single test node
                is_continuation = isinstance(entity.node.reference.pointer, ContinuationReferencePrefix)
                if is_continuation:
                    for test in tests:
                        if test.reference.reference.value == entity.reference:
                            test.setup_assertions += entity.node.setup_assertions
                            break
                else:
                    tests.append(entity.node)
            else:
                raise Exception(f'Unexpected node {entity.node}')
        if setup_stack:
            error_msg = 'Found setups without porpuse, those must be used before an assertion:\n'
            for setup in setup_stack:
                error_msg += f'in line {setup.line}\n'
            error(message=error_msg)
        return tests

    def build_constants_node(self) -> Constants:
        """Build contants node"""

        # This appends constants added during
        # running time via command line.
        #
        # # Constants
        # VERBOSE_DEBUG="| hexdump -C"
        # .
        # .
        # .
        # TEMP_DIR="/tmp"

        result = Constants(constants=[])

        # Append default VERBOSE_DEBUG constant
        #
        # NOTE: BatsppOpts.verbose_debug are used to
        #       default debug, for now is equivalent to hexdump_debug.
        value = ''
        if self.args.debug:
            value = self.args.debug
        elif self.opts.verbose_debug or self.opts.hexdump_debug:
            # More information about hexdump command:
            # - https://linoxide.com/linux-hexdump-command-examples/
            value = '| hexdump -C'
        token = build_text_node(f'{VERBOSE_DEBUG}="{value}"')
        result.constants.append(token)

        # Append TEMP_DIR constant
        value = self.args.temp_dir if self.args.temp_dir else '/tmp'
        token = build_text_node(f'{TEMP_DIR}="{value}"')
        result.constants.append(token)

        # Append COPY_DIR constant
        if self.args.copy_dir:
            token = build_text_node(f'{COPY_DIR}="{self.args.copy_dir}"')
            result.constants.append(token)

        return result

    def is_referenced_before_assignment(self, reference: str) -> bool:
        """Check reference is before assignment"""
        if reference is None:
            return True
        for entity in self._entities:
            if isinstance(entity.node, Test):
                if entity.reference == reference:
                    return False
        return True

    def analize(
            self,
            tree: ASTnode,
            opts: BatsppOpts = BatsppOpts(),
            args: BatsppArgs = BatsppArgs(),
            ) -> None:
        """Analize the semantic of the code, return modified tree, opts and args"""
        timer = Timer()
        timer.start()
        #
        self.opts = opts
        self.args = args
        self._entities = []
        self.visit(tree)
        #
        debug.trace(5, f'_SemanticAnalizer.analize() in {timer.stop()} seconds')
        return tree, opts, args

semantic_analizer = _SemanticAnalizer()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
