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

# Bash testing utils settings
SRC_PATH = __file__.rsplit('/', 1)[0]
TESTING_UTILS_PATH = SRC_PATH + '/testing_utils.bash'
DEBUG_FUNCTION = 'print_debug'
RUN_TEST_FUNCTION = 'run_test'
SUMMARY_FUNCTION = 'print_summary'

# Another function names
SETUP_FUNCTION = 'run_setup'
TEARDOWN_FUNCTION = 'run_teardown'

BATSPP_EXTENSION = 'batspp'
TEST_OUTPUT_INTERPRETER = 'bash'

# Runners
BATS = 'bats'
BASH = 'bash'

if __name__ == '__main__':
    warning_not_intended_for_cmd()
