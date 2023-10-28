#!/usr/bin/env python3
#
# Bats interpreter module
#

"""
Bats interpreter module
"""

# Standard packages
## NOTE: this is empty for now

# Installed packages
from mezcla import debug

# Local packages
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )
from batspp._interpreter import (
    Interpreter, flatten_str
    )
from batspp._ast_node import (
    Test, SetupAssertion,
    )
from batspp._settings import (
    SETUP_FUNCTION, TEARDOWN_FUNCTION,
    )

class BatsInterpreter(Interpreter):
    """
    Interpreter class to create tests using the Bats testing framework
    """

    def __init__(self):
        super().__init__()

    def build_test_header(self, test_name:str) -> str:
        """Build test header"""
        result = (
            f'@test "{test_name}" {{\n'
            f'    {SETUP_FUNCTION} "{flatten_str(test_name)}"\n'
            )
        return result

    def build_test_footer(self, test_name:str) -> str:
        """Build test footer"""
        result = (
            '\n'
            f'    {TEARDOWN_FUNCTION}\n'
            '}\n\n'
            )
        return result

    def build_assertion(
            self,
            operator:str,
            actual:str,
            expected:str,
            ) -> str:
        """
        Build assertion
        """
        actual = actual.replace('\n', '')
        expected = repr(expected.strip().rstrip('\n') + '\n')
        # Set debug
        debug_cmd = ''
        if not self.opts.omit_trace:
            debug_cmd = (
                '\tshopt -s expand_aliases\n'
                f'\tprint_debug "$({actual})" "$(echo -e {expected})"\n'
                )
        # Unify everything
        result = (
            f'{debug_cmd}'
            f'\t[ "$({actual})" {operator} "$(echo -e {expected})" ]\n'
            )
        debug.trace(7, f'interpreter.build_assertion(operator={operator}, actual={actual}, expeted={expected}) => {result}')
        return result

bats_interpreter = BatsInterpreter()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
