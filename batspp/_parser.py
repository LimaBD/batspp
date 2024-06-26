#!/usr/bin/env python3
#
# Parser module
#
# This module is responsible for building
# an abstract syntax tree (AST) for Batspp
#

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
from batspp._exceptions import (
    error, warning_not_intended_for_cmd,
    )
from batspp._token import (
    PESO, GREATER, SETUP, TEARDOWN,
    TEST, POINTER, CONTINUATION, ASSERT_EQ,
    ASSERT_NE, TEXT, EOF, NEW_LINE, GLOBAL,
    )
from batspp._ast_node import (
    ASTnode, TestSuite, TestOrSetup, GlobalTeardown,
    GlobalSetup, Setup, Test, ContinuationReferencePrefix,
    TestReference, SetupReference, CommandAssertion,
    Assertion, Command, CommandExtension, Text,
    MultilineText, ArrowAssertion, StandaloneCommands,
    SetupAssertion,
    )
from batspp._timer import Timer
from batspp.batspp_args import (
    BatsppArgs,
    )
from batspp.batspp_opts import (
    BatsppOpts,
    )

def copy_with_nested_lists(list_to_copy:list) -> list:
    """Copy a list with nested lists, better than using list.copy(), [:]
       because this copies the nested lists too, and better than a deepcopy
       because only copy a limited deep level"""
    result_copy = list_to_copy[:]
    for i, item in enumerate(result_copy):
        if isinstance(item, list):
            result_copy[i] = item[:]
    return result_copy

class _RuleState:
    """Rule state class"""

    def __init__(
            self,
            nodes:list=[],
            in_loop:bool=False,
            ) -> None:
        """init rule state"""
        self.nodes = nodes
        self.in_loop = in_loop

class _Rule:
    """Grammar rule class"""

    def __init__(self, resulting_ast_node:ASTnode, alias='') -> None:
        """Initialize a grammar rule"""
        # This is the AST node type that will be generated by this rule
        self._resulting_ast_node = resulting_ast_node
        # Alias is used for show the rule name in error messages
        if alias:
            self._alias = alias
        elif resulting_ast_node:
            self._alias = resulting_ast_node.__name__
        else:
            self._alias = 'UnnamedRule'
        self._alias = alias if alias else resulting_ast_node.__name__
        # Instructions are a list of tuples with a function and its parameters
        # that will be executed in order to build the AST tree from a list of tokens.
        self._instructions = []
        # Generated child nodes will be appended to the base AST node generated by this rule.
        #    resulting_ast_node
        #    /                \
        # child_node_1 ... child_node_N
        self._generated_child_nodes = []
        # This is used for loop instructions, determine if the child node should
        # be appended to the child nodes or in a list, used for loop instructions.
        #   resulting_ast_node
        #  /                \
        # child_node_N ... [child_node_N+1 ... ]
        self._running_loop_instruction = False
        # This is used when multiple parent rules use this rule,
        # avoid mix the states of every call to this rule.
        self._state_stack = []
        # List of tokens to be parsed
        self.tokens = []
        # This used for print debug messages
        self._debug_deep_level = 1

    def expect(self, token_or_rule) -> '_Rule':
        """Expect a token or another rule.\n
           Equivalent to regex: TOKEN_OR_RULE"""
        self._append_instruction(self._run_expect, token_or_rule)
        return self

    def optionally(self, token_or_rule) -> '_Rule':
        """Optionally expect a token or another rule.\n
           Equivalent to regex: TOKEN_OR_RULE?"""
        self._append_instruction(self._run_optionally, token_or_rule)
        return self

    def zero_or_more(self, token_or_rule) -> '_Rule':
        """Expect zero or N times a token or another rule.\n
           Equivalent to regex: TOKEN_OR_RULE*"""
        expected = token_or_rule
        not_expected = None # this is added with until()
        self._append_instruction(self._run_zero_or_more, (expected, not_expected))
        return self

    def one_or_more(self, token_or_rule) -> '_Rule':
        """Expect at least one or N times a token or another rule.\n
           Equivalent to regex: TOKEN_OR_RULE+"""
        expected = token_or_rule
        not_expected = None # this is added with until()
        self._append_instruction(self._run_one_or_more, (expected, not_expected))
        return self

    def expect_some_of(self, *tokens_or_rules) -> '_Rule':
        """Expect some of a token or another rule.\n
           Equivalent to regex: (TOKEN_OR_RULE1 | TOKEN_OR_RULE2 | ...)"""
        self._append_instruction(self._run_expect_some_of, tokens_or_rules)
        return self

    def ignore_next(self, token_or_rule) -> '_Rule':
        """Ignore next specified tokens or rules N times.\n
           Equivalent to regex: (?!TOKEN_OR_RULE*)"""
        self._append_instruction(self._run_ignore_next, token_or_rule)
        return self

    def until(self, token_or_rule) -> '_Rule':
        """Adds to latest loop a condition rule to stop it"""
        assert isinstance(self._instructions[-1], tuple), 'until() must be used after a loop'
        # Note: remember that tuples are immutable!
        func, params = self._instructions[-1]
        expected, not_expected = params
        not_expected = token_or_rule
        self._instructions[-1] = (func, (expected, not_expected))
        return self

    def build_tree_from(self, tokens: list, debug_deep_level=0) -> ASTnode:
        """Build an AST tree from a list of tokens"""
        ## TODO: expecify that tuple(ASTnode, list) is returned
        self._push_state()
        self.tokens = tokens
        self._debug_deep_level = debug_deep_level + 1
        self._run_instructions()
        generated_ast_tree = None
        if self._resulting_ast_node:
            generated_ast_tree = self._resulting_ast_node(*self._generated_child_nodes)
        self._pop_state()
        return generated_ast_tree, self.tokens

    def _append_instruction(self, func, params) -> None:
        """Append an rule instruction to the stack"""
        self._instructions.append((func, params))

    def _run_instructions(self) -> None:
        """Run all rule instructions in stack"""
        self._print_debug('_run_instructions', '<start>')
        for func, params in self._instructions:
            if isinstance(params, tuple):
                func(*params)
            else:
                func(params)
        self._print_debug('_run_instructions', '<stop>')

    def _push_state(self) -> None:
        """Save current state of this rule to the stack"""
        new_state = _RuleState(
            nodes=self._generated_child_nodes,
            in_loop=self._running_loop_instruction
        )
        self._state_stack.append(new_state)
        self._reset_state()

    def _pop_state(self) -> None:
        """Pop current state of this rule from the stack"""
        if self._state_stack:
            last_state = self._state_stack.pop()
            self._generated_child_nodes = last_state.nodes
            self._running_loop_instruction = last_state.in_loop
        else:
            self._reset_state()

    def _reset_state(self) -> None:
        """Reset current state of this rule"""
        self._generated_child_nodes = []
        self._running_loop_instruction = False

    def _eat_token(self, token) -> None:
        """Eat a specific token from the tokens list, or raise an error"""
        def print_debug(result):
            self._print_debug('_eat_token', f'{token} <{result}>')
        if self.tokens[0].variant == token:
            print_debug('ok')
            self._append_child_node(self.tokens[0])
            self.tokens = self.tokens[1:]
        else:
            print_debug('failed')
            error(
                message=f'Expected "{token}" but got "{self.tokens[0].variant}"',
                text_line=self.tokens[0].data.text_line,
                line=self.tokens[0].data.line,
                column=self.tokens[0].data.column,
                )

    def _is_rule_followed(self, token_or_rule) -> bool:
        """Check if the next tokens follow a rule or match token without consuming them."""
        self._print_debug('_is_rule_followed', str(token_or_rule))
        result = False
        tokens_backup = copy_with_nested_lists(self.tokens)
        children_backup = copy_with_nested_lists(self._generated_child_nodes)
        try:
            self._run_expect(token_or_rule)
            result = True
        except SyntaxError:
            pass
        self.tokens = tokens_backup
        self._generated_child_nodes = children_backup
        return result

    def _run_expect(self, token_or_rule) -> None:
        """Run a expect rule"""
        def print_debug(result):
            self._print_debug('_run_expect', f'{token_or_rule} <{result}>')
        if isinstance(token_or_rule, _Rule):
            print_debug('running child tree')
            child_tree, self.tokens = token_or_rule.build_tree_from(self.tokens, self._debug_deep_level)
            self._append_child_node(child_tree)
        elif isinstance(token_or_rule, str):
            print_debug('going to eat')
            self._eat_token(token_or_rule)
        else:
            print_debug('failed')
            raise Exception(f'Expected a Rule or Token but got {token_or_rule}')

    def _append_child_node(self, node: ASTnode) -> None:
        """Append a child node to the generated child nodes list"""
        self._print_debug('_append_child_node', f'{node}')
        # Loop instructions store a list of children instead of a single child node
        if self._running_loop_instruction:
            empty = not self._generated_child_nodes
            no_list = not isinstance(self._generated_child_nodes[-1], list)
            if empty or no_list:
                raise Exception('Not appended a list when started running a loop')
            self._generated_child_nodes[-1].append(node)
        else:
            self._generated_child_nodes.append(node)

    def _run_optionally(self, token_or_rule) -> None:
        """Run a optionally rule if next tokens match,
           otherwise append a 'None' to the generated
           child nodes list and continue."""
        self._print_debug('_run_optionally', f'{token_or_rule}')
        tokens_backup = copy_with_nested_lists(self.tokens)
        children_backup = copy_with_nested_lists(self._generated_child_nodes)
        try:
            self._run_expect(token_or_rule)
        except SyntaxError:
            self.tokens = tokens_backup
            self._generated_child_nodes = children_backup
            self._append_child_node(None)

    def _run_zero_or_more(self, expected, not_expected) -> None:
        """Run EXPECTED rule zero or more times until NOT_EXPECTED is found"""
        def print_debug(status):
            self._print_debug('_run_zero_or_more', f'{expected} <{status}>')
        self._setup_loop_instruction()
        print_debug('starting')
        while self.tokens:
            print_debug('loop')
            if not_expected is not None:
                if self._is_rule_followed(not_expected):
                    print_debug('not-expected found')
                    break
            try:
                self._run_expect(expected)
                print_debug('ok')
                continue # not necessary, but more readable
            except SyntaxError:
                print_debug('failed')
                break
        self._teardown_loop_instruction()

    def _run_one_or_more(self, expected, not_expected) -> None:
        """Run EXPECTED rule one or more times until NOT_EXPECTED is found"""
        self._print_debug('_run_one_or_more', f'{expected}, {not_expected} <starting>')
        self._setup_loop_instruction()
        if not_expected is not None:
            if self._is_rule_followed(not_expected):
                self._print_debug('_run_one_or_more', f"{not_expected} <not-expected found>")
                raise SyntaxError(f'Expected "{expected}" but got "{not_expected}"')
        self._run_expect(expected)
        self._run_zero_or_more(expected, not_expected)
        self._teardown_loop_instruction()
        self._print_debug('_run_one_or_more', f"{expected} <finished>")

    def _setup_loop_instruction(self) -> None:
        """Setup this rule to START a loop instruction"""
        if not self._running_loop_instruction:
            self._generated_child_nodes.append([])
        self._running_loop_instruction = True

    def _teardown_loop_instruction(self) -> None:
        """Setup this rule to END a loop instruction"""
        self._running_loop_instruction = False

    def _run_expect_some_of(self, *tokens_or_rules) -> None:
        """Expect at least any TOKENS_OR_RULES next"""
        def print_debug(branch):
            self._print_debug('_run_expect_some_of', f'{tokens_or_rules} <{branch}>')
        print_debug('starting')
        ## TODO: refactor, decide what branch of expected rules go without run entire rule first
        for token_or_rule in tokens_or_rules:
            print_debug(f'checking {token_or_rule}')
            try:
                self._run_expect(token_or_rule)
                print_debug(f'{token_or_rule} ok')
                return
            except SyntaxError:
                print_debug(f'{token_or_rule} failed')
                continue # not necessary, but more readable
        error(
            message=f'Expected some of "{tokens_or_rules}" but got "{self.tokens[0].variant}"',
            text_line=self.tokens[0].data.text_line,
            line=self.tokens[0].data.line,
            column=self.tokens[0].data.column,
            )

    def _run_ignore_next(self, token_or_rule) -> None:
        """Advance TOKEN_OR_RULE, but don't append any child node"""
        children_backup = copy_with_nested_lists(self._generated_child_nodes)
        while self.tokens:
            self._print_debug('_run_ignore_next', f'{token_or_rule} <running loop>')
            try:
                self._run_expect(token_or_rule)
            except SyntaxError:
                break
        self._generated_child_nodes = children_backup

    def _print_debug(self, method_name:str, notes:str) -> None:
        """Print debug information"""
        # Optimization shortcut if debugging is not required
        # This makes the parser x1.6 faster
        if debug.trace_level < 6:
            return
        #
        variant = self.tokens[0].variant if self.tokens else 'None'
        line_number = self.tokens[0].data.line if self.tokens else -1
        debug.trace(7, (
            f'{variant} '
            f'(l {str(line_number)})\t'
            f'{">" * self._debug_deep_level}\t'
            f'{self}.{method_name}:\t'
            f'{notes}'
        ))

    def __repr__(self):
        return self._alias

class _Parser:
    """Batspp parser class"""

    def build_grammar(
            self,
            embedded_tests:bool,
            has_arrow_assertion:bool,
            greater_token_present:bool,
            ) -> _Rule:
        """Returns the grammar rules for Batspp.\n
           If EMBEDDED_TESTS is True, the grammar rules will be
           modified to allow embedded tests.\n
           If HAS_ARROW_ASSERTION is False, the grammar rules
           will be optimized with shortcuts, same with
           GREATER_TOKEN_PRESENT"""
        timer = Timer()
        timer.start()

        # Batspp complete grammar
        #
        # this is dinamic and changes depending if
        # the tests are embedded or not, those changes
        # are indicated with parenthesis.
        #
        # e.g.: "(normal)   NAME : RULE"
        # e.g.: "(embedded) NAME : OTHER RULE"

        # (normal)   test_suite : global_setup? (test_or_setup)+ global_teardown? EOF
        # (embedded) test_suite : (?!any_text)* test_suite (?!any_text)*
        #
        # (normal)   test_or_setup : test | setup
        # (embedded) test_or_setup : (?!any_text)* test_or_setup (?!any_text)*
        #
        # any_text : multiline_text | NEW_LINE
        #
        # global_setup : GLOBAL? SETUP standalone_commands
        # global_teardown : GLOBAL? TEARDOWN standalone_commands
        # test : test_reference? (setup_assertion)+ (?!NEW_LINE)*
        # setup_assertion : setup? assertion
        # setup : setup_reference? standalone_commands
        #
        # standalone_commands : command+ [^command_assertion] (?!NEW_LINE)*
        #
        # setup_reference : SETUP POINTER TEXT
        # test_reference : (TEST | continuation_reference_prefix) TEXT
        # continuation_reference_prefix : CONTINUATION POINTER
        #
        # assertion : command_assertion | arrow_ne_assertion | arrow_eq_assertion
        # arrow_eq_assertion : TEXT ASSERT_EQ TEXT+ multiline_text
        # arrow_ne_assertion : TEXT ASSERT_NE TEXT+ multiline_text
        # command_assertion : command multiline_text
        #
        # command : PESO TEXT command_extension* (?!NEW_LINE)*
        # command_extension : GREATER TEXT
        #
        # multiline_text : text+ [^end_of_mtext]
        # end_of_mtext : arrow_assertion_start | command_start
        # arrow_assertion_start : NEW_LINE* TEXT (ASSERT_EQ | ASSERT_NE)
        # command_start : NEW_LINE+ PESO
        #
        # (normal)   text : TEXT | NEW_LINE
        # (embedded) text : TEXT

        # Notes:
        # - the order of the rules are inverted, the last rule is
        #   the first to be declared due to nested rules.
        # - carefull referencing the same rule in another rules,
        #   it can cause problems when building the ast node object.

        text = None
        if embedded_tests:
            text = TEXT
        else:
            text = _Rule(Text).expect_some_of(TEXT, NEW_LINE)

        # Optimization shortcuting arrow assertion,
        # due that arrow assertion is less used than
        # command assertions
        command_start = _Rule(None, alias="command_start") \
            .one_or_more(NEW_LINE).expect(PESO)
        end_of_mtext = command_start
        if has_arrow_assertion:
            arrow_assertion_start = _Rule(None, alias="arrow_assertion_start") \
                .zero_or_more(NEW_LINE).expect(TEXT).expect_some_of(ASSERT_EQ, ASSERT_NE)
            end_of_mtext = _Rule(None, alias="end_of_mtext") \
                .expect_some_of(arrow_assertion_start, command_start)
        multiline_text = _Rule(MultilineText) \
            .one_or_more(text).until(end_of_mtext)

        # Optimization shortcuting command extension,
        # due that command extension is not used in
        # most of the tests
        command = _Rule(Command) \
            .expect(PESO).expect(TEXT)
        if greater_token_present:
            command_extension = _Rule(CommandExtension) \
                .expect(GREATER).expect(TEXT)
            command = command.zero_or_more(command_extension)
        command = command.ignore_next(NEW_LINE)

        command_assertion = _Rule(CommandAssertion) \
            .expect(command).expect(multiline_text)
        assertion = command_assertion
        if has_arrow_assertion:
            arrow_eq_assertion = _Rule(ArrowAssertion) \
                .expect(TEXT).expect(ASSERT_EQ).expect(multiline_text)
            arrow_ne_assertion = _Rule(ArrowAssertion) \
                .expect(TEXT).expect(ASSERT_NE).expect(multiline_text)
            assertion = _Rule(Assertion) \
                .expect_some_of(command_assertion, arrow_eq_assertion, arrow_ne_assertion)

        continuation_reference_prefix = _Rule(ContinuationReferencePrefix) \
            .expect(CONTINUATION).expect(POINTER)
        test_reference = _Rule(TestReference) \
            .expect_some_of(TEST, continuation_reference_prefix).expect(TEXT)
        setup_reference = _Rule(SetupReference) \
            .expect(SETUP).expect(POINTER).expect(TEXT)

        standalone_commands = _Rule(StandaloneCommands) \
            .one_or_more(command).until(command_assertion).ignore_next(NEW_LINE)

        setup = _Rule(Setup) \
            .optionally(setup_reference).expect(standalone_commands)
        setup_assertion = _Rule(SetupAssertion) \
            .optionally(setup).expect(assertion)
        test = _Rule(Test) \
            .optionally(test_reference) \
            .one_or_more(setup_assertion).ignore_next(NEW_LINE)
        global_teardown = _Rule(GlobalTeardown) \
            .optionally(GLOBAL).expect(TEARDOWN).expect(standalone_commands)
        global_setup = _Rule(GlobalSetup) \
            .optionally(GLOBAL).expect(SETUP).expect(standalone_commands)

        # This rule is only used with embedded tests to reduce
        # functions calls we can avoid it if is not used
        any_text = None
        if embedded_tests:
            any_text = _Rule(None, alias="any_text") \
                .expect_some_of(multiline_text, NEW_LINE)

        test_or_setup = _Rule(TestOrSetup)
        if embedded_tests:
            test_or_setup = test_or_setup.ignore_next(any_text)
        test_or_setup = test_or_setup \
            .expect_some_of(test, setup)
        if embedded_tests:
            test_or_setup = test_or_setup.ignore_next(any_text)

        test_suite = _Rule(TestSuite) \
            .ignore_next(any_text if embedded_tests else NEW_LINE) \
            .optionally(global_setup) \
            .one_or_more(test_or_setup).optionally(global_teardown) \
            .expect(EOF)

        debug.trace(5, f'Parser.build_grammar(...) in {timer.stop()} seconds')
        return test_suite

    def parse(
            self,
            tokens: list,
            opts: BatsppOpts = None,
            args: BatsppArgs = None
            ) -> ASTnode:
        """Builds an Abstract Syntax Tree (AST) from TOKENS list following the Batspp grammar."""
        timer = Timer()
        timer.start()
        #
        grammar = self.build_grammar(
            opts.embedded_tests,
            opts.has_arrow_assertion,
            opts.greater_token_present
            )
        tree, _ = grammar.build_tree_from(tokens)
        #
        debug.trace(5, f'Parser.parse() in {timer.stop()} seconds')
        return tree, opts, args

parser = _Parser()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
