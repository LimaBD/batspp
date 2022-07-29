#!/usr/bin/env python3
#
# Batspp options module
#


"""Batspp options module"""


# Local modules
from exceptions import assert_type


class BatsppOpts:
    """Batspp test related options"""

    def __init__(self,
                 embedded_tests: bool = False,
                 verbose_debug: bool = False,
                 hexview_debug: bool = False,
                 omit_trace: bool = False,
                 disable_aliases: bool = False) -> None:

        # Check for embedded_tests
        assert_type(embedded_tests, bool)
        self.embedded_tests = embedded_tests

        # Check for verbose_debug
        assert_type(verbose_debug, bool)
        self.verbose_debug = verbose_debug

        # Check for verbose_debug
        assert_type(hexview_debug, bool)
        self.hexview_debug = hexview_debug

        # Check for omit_trace
        assert_type(omit_trace, bool)
        self.omit_trace = omit_trace

        # Check for disable_aliases
        assert_type(disable_aliases, bool)
        self.disable_aliases = disable_aliases
