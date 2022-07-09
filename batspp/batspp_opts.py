#!/usr/bin/env python3
#
# Batspp options module
#


"""Batspp options module"""


class BatsppOpts:
    """Batspp test related options"""

    def __init__(self,
                 embedded_tests: bool = False,
                 verbose_debug: bool = False,
                 omit_trace: bool = False,
                 disable_aliases: bool = False) -> None:
        __error_string = 'invalid type'

        # Check for embedded_tests
        assert isinstance(embedded_tests, bool), __error_string
        self.embedded_tests = embedded_tests

        # Check for verbose_debug
        assert isinstance(verbose_debug, bool), __error_string
        self.verbose_debug = verbose_debug

        # Check for omit_trace
        assert isinstance(omit_trace, bool), __error_string
        self.omit_trace = omit_trace

        # Check for disable_aliases
        assert isinstance(disable_aliases, bool), __error_string
        self.disable_aliases = disable_aliases
