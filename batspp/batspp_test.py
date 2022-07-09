#!/usr/bin/env python3
#
# Batspp Test module
#


"""Batspp Test module"""


# Installed packages
from mezcla import debug
from mezcla import glue_helpers as gh


# Local modules
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from batspp_opts import BatsppOpts
from batspp_args import BatsppArgs


class BatsppTest:
    """
    This is responsible to build and run Batspp test
    """

    def __init__(self) -> None:

        # Global states
        self.content = ''
        self.path = ''

    def build(self,
              text: str,
              opts: BatsppOpts = BatsppOpts(),
              args: BatsppArgs = BatsppArgs()) -> None:
        """
        Build tests from TEXT,
        with OPTS can be setted test options and with
        ARGS can be setted test arguments
        """

        # Process tests
        tokens = Lexer().tokenize(text, opts.embedded_tests)
        tree = Parser().parse(tokens)
        self.content = Interpreter().interpret(tree, opts=opts, args=args)

        assert self.content, 'No tests founded'

    def get_tests(self) -> str:
        """Return tests"""
        debug.trace(7, 'Test.get_tests()')
        return self.content

    def save(self, path: str) -> None:
        """Save tests on PATH"""
        debug.trace(7, f'Test.save({path})')

        assert path, 'PATH string cannot be empty'
        assert self.content, 'Tests must be builded, try build() method'

        self.path = path

        gh.write_file(path, self.content)
        gh.run(f'chmod +x {path}')

    def run(self, opts:str='') -> str:
        """
        Return stdout from runned tests
        with OPTS (options) can be used aditional options to run
        """
        debug.trace(7, f'Test.run() on path={self.path}')

        assert self.path, 'Tests must be saved, try save() method'

        # Check for root permissions
        sudo = 'sudo' if 'sudo' in self.content else ''

        return gh.run(f'{sudo} bats {opts} {self.path}')
