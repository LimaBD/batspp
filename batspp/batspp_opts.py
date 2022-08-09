#!/usr/bin/env python3
#
# Batspp options module
#


"""Batspp options module"""


# Local modules
from batspp._exceptions import assert_type


class BatsppOpts:
    """Batspp test related options"""

    def __init__(self,
                 embedded_tests: bool = False,
                 verbose_debug: bool = False,
                 hexdump_debug: bool = False,
                 omit_trace: bool = False,
                 disable_aliases: bool = False) -> None:

        # Check for embedded_tests
        assert_type(embedded_tests, bool)
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
