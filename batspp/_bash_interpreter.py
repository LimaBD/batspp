#!/usr/bin/env python3
#
# Bash interpreter module
#

"""
Bash interpreter module
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
    Test, SetupAssertion, TestSuite,
    )
from batspp._settings import (
    SETUP_FUNCTION, TEARDOWN_FUNCTION,
    RUN_TEST_FUNCTION, DEBUG_FUNCTION,
    SUMMARY_FUNCTION,
    )

class BashInterpreter(Interpreter):
    """
    Interpreter class using Bash directly to create tests
    """

    def __init__(self):
        super().__init__()

    # pylint: disable=invalid-name
    def visit_TestSuite(self, node: TestSuite) -> str:
        """Visit TestSuite NODE"""
        result = super().visit_TestSuite(node)
        result += f'{SUMMARY_FUNCTION}\n'
        return result

    def build_test_header(self, test_name:str) -> str:
        """Build test header"""
        flatten_name = flatten_str(test_name)
        result = (
            f'function {flatten_name} {{\n'
            f'    exec > /dev/null # avoid setup commands to show output\n'
            f'    {SETUP_FUNCTION} "{flatten_name}"\n'
            )
        return result

    def build_test_footer(self, test_name:str) -> str:
        """Build test footer"""
        flatten_name = flatten_str(test_name)
        result = (
            '\n'
            f'    {TEARDOWN_FUNCTION}\n'
            '    exec >/dev/tty # restore stdout\n'
            '    return 0\n'
            '}\n'
            f'{RUN_TEST_FUNCTION} "{test_name}" "{flatten_name}"\n\n'
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
                '    shopt -s expand_aliases\n'
                )
        # Unify everything
        result = (
            f'{debug_cmd}'
            '    exec >/dev/tty # restore stdout\n'
            f'    if [ "$({actual})" {operator} "$(echo -e {expected})" ]\n'
            '    then\n'
            '        : # keep\n'
            '    else\n'
            f'        {DEBUG_FUNCTION} "$({actual})" "$(echo -e {expected})"\n'
            '        return 1\n'
            '    fi\n'
            '    exec > /dev/null # next setup commands should not show output\n'
            )
        debug.trace(7, f'interpreter.build_assertion(operator={operator}, actual={actual}, expeted={expected}) => {result}')
        return result

bash_interpreter = BashInterpreter()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
