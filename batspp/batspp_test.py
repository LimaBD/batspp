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
from batspp._jupyter_to_batspp import jupyter_to_batspp
from batspp._bats_interpreter import bats_interpreter
from batspp._bash_interpreter import bash_interpreter
from batspp._settings import (
    BATSPP_EXTENSION,
    BASH, BATS,
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

def resolve_path(path:str, alternative:str, extension:str) -> str:
    """
    Resolve PATH based on ALTERNATIVE filename and EXTENSION
    \n
    resolve_path('/folder/', '/project/folder/test_file.batspp', 'bash')
    => '/folder/generated_test_file.bash'
    """
    result = ''
    if not path:
        result = add_prefix_to_filename(alternative, 'generated_')
        result = replace_extension(result, extension)
    elif path.endswith('/'):
        result = merge_filename_into_path(alternative, path)
        result = add_prefix_to_filename(result, 'generated_')
        result = replace_extension(result, extension)
    else:
        result = path
    return result

def save_resolving_path(original_file, new_file, extension, content):
    """Save with exec permissions CONTENT to NEW_FILE,
       resolving NEW_FILE path based on ORIGINAL_FILE"""
    new_file = resolve_path(new_file, original_file, extension)
    save_with_permissions(new_file, content)

def save_with_permissions(file:str, content:str) -> None:
    """Save CONTENT to FILE with exec permissions"""
    gh.write_file(file, content)
    gh.run(f'chmod +x {file}')

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
        """Return transpiled Bash content from Batspp test FILE"""
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
        ## TODO: refactor with polymorfism but carefull with circular imports!
        interpreter = None
        if args.runner == BATS:
            interpreter = bats_interpreter
        elif args.runner == BASH:
            interpreter = bash_interpreter
        transpiled = interpreter.interpret(tree, opts=opts, args=args)

        # Save copy if requested
        if copy_path:
            save_resolving_path(file, copy_path, args.runner, transpiled)

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
           if OUTPUT is not provided or is a dir, a default is used 'generated_<file>.runner'"""
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
        # Get tests
        transpiled = self.transpile_to_bats(file, args=args, opts=opts)
        # Save in TMP to run
        temp_bats = f'{gh.get_temp_file()}.tmp'
        save_with_permissions(temp_bats, transpiled)
        # Save copy if requested
        if copy_path:
            save_resolving_path(file, copy_path, args.runner, transpiled)
        # Run
        sudo = 'sudo' if 'sudo' in transpiled else ''
        output = gh.run(f'{sudo} {args.runner} {args.run_opts} {temp_bats}')
        #
        debug.trace(5, f'BatsppTest.run() finished in {timer.stop()} seconds')
        return output

if __name__ == '__main__':
    warning_not_intended_for_cmd()
