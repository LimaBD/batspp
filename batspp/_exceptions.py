#!/usr/bin/env python3
#
# Exceptions module
#


"""
Exceptions module
"""


# Standard packages
import sys

# Installed packages
## NOTE: this is empty for now

# Local packages
## NOTE: this is empty for now


def error(
        message:str='',
        text_line:str='',
        line:int=None,
        column:str=None,
        ) -> None:
    """Raise exception"""
    ## TODO: limit text_line if it is very long

    output = ''
    output += f'{message}' if message else ''
    output += f'\nline {line}: {text_line}' if text_line and line else ''
    output += f'\n             {" " * column}^' if column else ''

    raise Exception(output)


def warning(message: str) -> None:
    """Prints to stderr MESSAGE starting with 'Warning:' and ending with newline"""
    sys.stderr.write(f"Warning: {message}\n")


def warning_not_intended_for_cmd() -> None:
    """Prints a warning useful to modules that arent intended for command-line use"""
    warning("not intended for command-line use")


def assert_type(var: any, expected_type: any) -> None:
    """Assert variable type"""
    assert isinstance(var, expected_type), f'expected type {expected_type} but founded {type(var)}'


if __name__ == '__main__':
    warning_not_intended_for_cmd()
