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
## NOTE: this is empty for now

# Local packages
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )
from batspp._interpreter import Interpreter

class BatsInterpreter(Interpreter):

    ## TODO: implement
    pass

bats_interpreter = BatsInterpreter()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
