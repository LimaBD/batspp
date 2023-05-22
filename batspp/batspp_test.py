#!/usr/bin/env python3
#
# Batspp Test module
#


"""Batspp test module"""


# Standard packages
from re import search as re_search

# Installed packages
from mezcla import glue_helpers as gh

# Local packages
from batspp._lexer import Lexer
from batspp._parser import Parser
from batspp._interpreter import Interpreter
from batspp._ipynb_to_batspp import IpynbToBatspp
from batspp._settings import (
    BATSPP_EXTENSION, BATS_EXTENSION
)
from batspp.batspp_opts import BatsppOpts
from batspp.batspp_args import BatsppArgs
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )


def add_prefix_to_filename(file:str, prefix:str) -> str:
    """Adds PREFIX to FILE path"""
    return f'{gh.dir_path(file)}/{prefix}{gh.basename(file)}'


def merge_filename_into_path(filename:str, path:str) -> str:
    """Merge FILENAME into PATH, e.g. /etc/passwd /home/ => /home/passwd """
    assert filename and path, 'FILENAME or PATH cannot be empty'
    assert path.endswith('/'), 'PATH must end with "/".'
    return f'{path}{gh.basename(filename)}'


def replace_extension(filename:str, extension:str) -> str:
    """Replace current FILENAME extension with EXTENSION"""
    current_extension = re_search(r'(?:\.\w+)+', filename).group()
    filename = gh.remove_extension(filename, current_extension)
    return f'{filename}.{extension}'


def resolve_path(path:str, alternative:str) -> str:
    """Resolve PATH based on ALTERNATIVE filename"""
    result = ''
    if not path:
        result = add_prefix_to_filename(alternative, 'generated_')
        result = replace_extension(result, BATS_EXTENSION)
    elif path.endswith('/'):
        result = merge_filename_into_path(alternative, path)
        result = add_prefix_to_filename(result, 'generated_')
        result = replace_extension(result, BATS_EXTENSION)
    else:
        result = path
    return result


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
        self.ipynb_to_text = IpynbToBatspp()

    def _is_not_batspp_file(self, file:str) -> bool:
        """Whether is FILE is a batspp test file"""
        return not file.endswith(f'.{BATSPP_EXTENSION}')

    def is_ipynb_file(self, file:str) -> bool:
        """Whether is FILE is a Jupyter notebook file"""
        return file.endswith('.ipynb')

    def is_not_ipynb_file(self, file:str) -> bool:
        """Whether is FILE is not a Jupyter notebook file"""
        return not self.is_ipynb_file(file)

    def transpile_to_bats(
            self,
            file: str,
            args: BatsppArgs = BatsppArgs(),
            opts: BatsppOpts = BatsppOpts()
            ) -> str:
        """Return transpiled Bats content from Batspp test FILE"""
        assert file, 'File path cannot be empty'

        # Check for embedded tests
        if opts.embedded_tests is None:
            opts.embedded_tests = self._is_not_batspp_file(file) and self.is_not_ipynb_file(file)

        # Check for sources files
        if opts.embedded_tests:
            if args.sources:
                args.sources.append(file)
            else:
                args.sources = [file]

        # Transpilation
        content = gh.read_file(file)
        content = self.ipynb_to_text.convert(content) if self.is_ipynb_file(file) else content
        tokens = self.lexer.tokenize(content, opts.embedded_tests)
        tree = self.parser.parse(tokens, opts.embedded_tests)
        result = self.interpreter.interpret(tree, opts=opts, args=args)

        return result

    def transpile_and_save_bats(
            self,
            file:str,
            output:str='',
            args: BatsppArgs = BatsppArgs(),
            opts: BatsppOpts = BatsppOpts()
            ) -> None:
        """Save Batspp transiled test FILE to OUTPUT path,
           if OUTPUT is not provided or is a dir, a default is used 'generated_<file>.bats'"""
        assert file, 'File path cannot be empty'
        output = resolve_path(output, file)
        transpiled_text = self.transpile_to_bats(file, args=args, opts=opts)
        gh.write_file(output, transpiled_text)
        gh.run(f'chmod +x {output}')

    def run(
            self,
            file:str,
            args: BatsppArgs = BatsppArgs(),
            opts: BatsppOpts = BatsppOpts()
            ) -> str:
        """Run Batspp test FILE and return result"""
        assert file, 'File path cannot be empty'
        temp_bats = f'{gh.get_temp_file()}.{BATS_EXTENSION}'
        self.transpile_and_save_bats(file, temp_bats, args=args, opts=opts)
        sudo = 'sudo' if 'sudo' in gh.read_file(temp_bats) else ''
        return gh.run(f'{sudo} bats {args.run_opts} {temp_bats}')


if __name__ == '__main__':
    warning_not_intended_for_cmd()
