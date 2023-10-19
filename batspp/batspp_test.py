#!/usr/bin/env python3
#
# Batspp Test module
#

"""Batspp test module"""

# Standard packages
from re import search as re_search

# Installed packages
from mezcla import glue_helpers as gh
from mezcla import debug

# Local packages
from batspp._lexer import lexer
from batspp._parser import parser
from batspp._semantic_analizer import semantic_analizer
from batspp._interpreter import interpreter
from batspp._jupyter_to_batspp import jupyter_to_batspp
from batspp._settings import (
    BATSPP_EXTENSION, BATS_EXTENSION
)
from batspp.batspp_opts import BatsppOpts
from batspp.batspp_args import BatsppArgs
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )
from batspp._timer import Timer
from batspp.batspp_args import (
    BatsppArgs,
    )
from batspp.batspp_opts import (
    BatsppOpts,
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

def save(original_file, new_file, content):
    """Save CONTENT to NEW_FILE, resolving NEW_FILE path based on ORIGINAL_FILE"""
    new_file = resolve_path(new_file, original_file)
    gh.write_file(new_file, content)
    gh.run(f'chmod +x {new_file}')

class BatsppTest:
    """
    This is responsible to parse and run Batspp tests
    """

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
            copy_path:str='',
            args: BatsppArgs = BatsppArgs(),
            opts: BatsppOpts = BatsppOpts()
            ) -> str:
        """Return transpiled Bats content from Batspp test FILE"""
        assert file, 'File path cannot be empty'
        timer = Timer()
        timer.start()

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
        content = jupyter_to_batspp.convert(content) if self.is_ipynb_file(file) else content
        tokens, opts, args = lexer.tokenize(content, opts=opts, args=args)
        tree, opts, args = parser.parse(tokens, opts=opts, args=args)
        tree, opts, args = semantic_analizer.analize(tree, opts=opts, args=args)
        transpiled = interpreter.interpret(tree, opts=opts, args=args)

        # Save copy if requested
        if copy_path:
            save(file, copy_path, transpiled)

        debug.trace(5, f'BatsppTest.transpile_to_bats() finished in {timer.stop()} seconds')
        return transpiled

    def transpile_and_save_bats(
            self,
            file:str,
            output:str='',
            args: BatsppArgs = BatsppArgs(),
            opts: BatsppOpts = BatsppOpts()
            ) -> None:
        """Save Batspp transiled test FILE to OUTPUT path,
           if OUTPUT is not provided or is a dir, a default is used 'generated_<file>.bats'"""
        _ = self.transpile_to_bats(file, copy_path=output, args=args, opts=opts)

    def run(
            self,
            file:str,
            copy_path:str='',
            args: BatsppArgs = BatsppArgs(),
            opts: BatsppOpts = BatsppOpts()
            ) -> str:
        """Run Batspp test FILE and return result"""
        timer = Timer()
        timer.start()

        transpiled = self.transpile_to_bats(file, args=args, opts=opts)
        # Save in TMP to run
        temp_bats = f'{gh.get_temp_file()}.{BATS_EXTENSION}'
        save(file, temp_bats, transpiled)
        # Save copy if requested
        if copy_path:
            save(file, copy_path, transpiled)
        # Run
        sudo = 'sudo' if 'sudo' in transpiled else ''
        output = gh.run(f'{sudo} bats {args.run_opts} {temp_bats}')

        debug.trace(5, f'BatsppTest.run() finished in {timer.stop()} seconds')
        return output

if __name__ == '__main__':
    warning_not_intended_for_cmd()
