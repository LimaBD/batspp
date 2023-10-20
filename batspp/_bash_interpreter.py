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
## NOTE: this is empty for now

# Local packages
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )
from batspp._interpreter import Interpreter

class BashInterpreter(Interpreter):

    ## TODO: implement
    pass

bash_interpreter = BashInterpreter()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
