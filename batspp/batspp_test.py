#!/usr/bin/env python3
#
# Batspp Test module
#


"""Batspp test module"""


# Standard packages
from re import search as re_search
from os import path as os_path
from datetime import datetime


# Installed packages
from mezcla import debug
from mezcla import glue_helpers as gh
from mezcla import system


# Local packages
from batspp._lexer import Lexer
from batspp._parser import Parser
from batspp._interpreter import Interpreter
from batspp._settings import (
    BATSPP_EXTENSION, BATS_EXTENSION
)
from batspp.batspp_opts import BatsppOpts
from batspp.batspp_args import BatsppArgs


class BatsppTest:
    """
    This is responsible to parse and run Batspp tests
    """

    def __init__(self) -> None:
        # Most used classes
        #
        # this avoid to instanciate a new class
        # every time that a tests file is parsed
        self.lexer = Lexer()
        self.parser = Parser()
        self.interpreter = Interpreter()

        # Global states
        self.opts = BatsppOpts()
        self.args = BatsppArgs()
        self.result_tests = ''
        self.initial_path = ''
        self.final_path = ''

    def set_options(self, opts: BatsppOpts) -> None:
        """Set options OPTS"""
        self.opts = opts

    def set_arguments(self, args: BatsppArgs) -> None:
        """Set arguments ARGS"""
        self.args = args

    def parse(self, text: str) -> None:
        """
        parse tests from TEXT
        """
        debug.trace(7, f'BatsppTest.parse({text})')

        assert text, 'TEXT cannot be empty'

        tokens = self.lexer.tokenize(text, self.opts.embedded_tests)
        tree = self.parser.parse(tokens, self.opts.embedded_tests)
        self.result_tests = self.interpreter.interpret(tree, opts=self.opts, args=self.args)

        if self.initial_path:
            assert self.result_tests, f'Not founded tests in file {self.initial_path}'
        assert self.result_tests, 'Not founded tests'

    def parse_file(self, file: str) -> None:
        """
        Open and parse FILE
        """
        debug.trace(7, f'BatsppTest.parse_file({file})')

        assert file, 'FILE cannot be empty'
        file = os_path.abspath(file)

        # Check for embedded tests
        #
        # Source the test file to load aliases and functions
        if not file.endswith(f'.{BATSPP_EXTENSION}'):
            if not self.opts.embedded_tests:
                self.opts.embedded_tests = True
            if self.args.sources:
                self.args.sources.append(file)
            else:
                self.args.sources = [file]

        self.parse(system.read_file(file))
        self.initial_path = file

    def get_tests(self) -> str:
        """Return tests"""
        debug.trace(7, 'BatsppTest.get_tests()')
        return self.result_tests

    def save(self, path: str) -> None:
        """
        Save tests on PATH,
        this could be an file name or directory (ending with [/])
        """
        debug.trace(7, f'Test.save({path})')

        assert path, 'PATH string cannot be empty'
        assert self.result_tests, 'no tests to save, try parse() or parse_file() methods'

        # Check if path is a folder
        #
        # By default the file name can be
        # - generated_<file>.bats
        # - generated_file_<timestamp>.bats
        if path.endswith('/'):
            file_name = ''
            if self.initial_path:
                file_name = re_search(r"\/(\w+)\.", self.initial_path).group(0)
            else:
                file_name = f'file_{datetime.now()}'
            path += f'generated_{file_name}.{BATS_EXTENSION}'

        self.final_path = path

        gh.write_file(self.final_path, self.result_tests)
        gh.run(f'chmod +x {self.final_path}')

    def run(self) -> str:
        """
        Run tests and return stdout
        """
        debug.trace(7, f'BatsppTest.run() on path={self.final_path}')

        assert self.final_path, 'Tests must be saved, try save() method'

        # Check for root permissions
        sudo = 'sudo' if 'sudo' in self.result_tests else ''

        return gh.run(f'{sudo} bats {self.args.run_opts} {self.final_path}')
