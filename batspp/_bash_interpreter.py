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
    Test, SetupAssertion,
    )
from batspp._settings import (
    SETUP_FUNCTION, TEARDOWN_FUNCTION,
    RUN_TEST_FUNCTION, DEBUG_FUNCTION,
    )

class BashInterpreter(Interpreter):
    """
    Interpreter class using Bash directly to create tests
    """

    def __init__(self):
        super().__init__()

    # pylint: disable=invalid-name
    def visit_Test(self, node: Test) -> str:
        """
        Visit Test NODE, also updates global class test title
        """
        name = self.visit(node.reference)
        flatten_name = flatten_str(name)
        # Test header
        # with call to a global setup function
        result = (
            f'function {flatten_name} {{\n'
            f'    {SETUP_FUNCTION} "{flatten_name}"\n'
            )
        # Visit assertions
        # Note that due to the semantic analyzer,
        # only tests should be here
        for t in node.setup_assertions:
            assert isinstance(t, SetupAssertion), 'Only SetupAssertion nodes should be at this point'
            result += self.visit(t)
        # Test footer
        # with call to a global teardown function
        result += (
            '\n'
            f'    {TEARDOWN_FUNCTION}\n'
            '    return 0\n'
            '}\n'
            f'{RUN_TEST_FUNCTION} "{name}" "{flatten_name}"\n\n'
            )
        debug.trace(7, f'interpreter.visit_Test(node={node}) => {result}')
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
            f'    if [ "$({actual})" {operator} "$(echo -e {expected})" ]\n'
            '    then\n'
            '        : # keep\n'
            '    else\n'
            f'        {DEBUG_FUNCTION} "$({actual})" "$(echo -e {expected})"\n'
            '        return 1\n'
            '    fi\n'
            )
        debug.trace(7, f'interpreter.build_assertion(operator={operator}, actual={actual}, expeted={expected}) => {result}')
        return result

bash_interpreter = BashInterpreter()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
