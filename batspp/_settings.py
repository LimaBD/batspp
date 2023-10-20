#!/usr/bin/env python3
#
# Settings
#
# This contains constants required
# by multiple local modules
#

"""Settings module"""

# Standard packages
## NOTE: this is empty for now

# Installed packages
## NOTE: this is empty for now

# Local packages
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )

BATSPP_EXTENSION = 'batspp'

TEST_OUTPUT_INTERPRETER = 'bash'

if __name__ == '__main__':
    warning_not_intended_for_cmd()
