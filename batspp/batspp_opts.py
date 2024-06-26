#!/usr/bin/env python3
#
# Batspp options module
#


"""Batspp options module"""


# Standard packages
## NOTE: this is empty for now

# Installed packages
## NOTE: this is empty for now

# Local packages
from batspp._exceptions import (
    assert_type, warning_not_intended_for_cmd,
    )


class BatsppOpts:
    """Batspp test options class, useful to share
       and set options between modules"""

    def __init__(
            self,
            embedded_tests: 'bool|None' = None,
            verbose_debug: bool = False,
            hexdump_debug: bool = False,
            omit_trace: bool = False,
            disable_aliases: bool = False,
            has_arrow_assertion: bool = False,
            greater_token_present: bool = False,
            ) -> None:

        # Check for embedded_tests
        assert_type(embedded_tests, (bool, type(None)))
        self.embedded_tests = embedded_tests

        # Check for verbose_debug
        assert_type(verbose_debug, bool)
        self.verbose_debug = verbose_debug

        # Check for verbose_debug
        assert_type(hexdump_debug, bool)
        self.hexdump_debug = hexdump_debug

        # Check for omit_trace
        assert_type(omit_trace, bool)
        self.omit_trace = omit_trace

        # Check for disable_aliases
        assert_type(disable_aliases, bool)
        self.disable_aliases = disable_aliases

        # Optimization flags
        assert_type(has_arrow_assertion, bool)
        self.has_arrow_assertion = has_arrow_assertion
        assert_type(greater_token_present, bool)
        self.greater_token_present = greater_token_present

if __name__ == '__main__':
    warning_not_intended_for_cmd()
