#!/usr/bin/env python3
#
# Exceptions module
#


"""
Exceptions module
"""


def error(message:str='',
          text_line:str='',
          line:int=None,
          column:str=None) -> None:
    """Raise exception"""
    ## TODO: limit text_line if it is very long

    output = ''
    output += f'{message}' if message else ''
    output += f'\nline {line}: {text_line}' if text_line and line else ''
    output += f'\n             {" " * column}^' if column else ''

    raise Exception(output)

def assert_type(var: any, expected_type: any) -> None:
    """Assert variable type"""
    assert isinstance(var, expected_type), f'expected type {expected_type} but founded {type(var)}'
