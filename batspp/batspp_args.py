#!/usr/bin/env python3
#
# Batspp arguments module
#

"""Batspp arguments module"""

# Standard packages
## NOTE: this is empty for now

# Installed packages
## NOTE: this is empty for now

# Local packages
from batspp._exceptions import (
    assert_type, warning_not_intended_for_cmd,
    )
from batspp._settings import (
    BATS, BASH,
    )

class BatsppArgs:
    """Batspp test arguments class, useful
       to share and set arguments between modules"""

    def __init__(
            self,
            sources: 'list|None' = None,
            temp_dir: str = '',
            visible_paths: 'list|None' = None,
            run_opts: str = '',
            copy_dir: str = '',
            debug: str = '',
            runner: str = 'bats',
            ) -> None:

        # Check for sources, filter empty sources
        assert_type(sources, (list, type(None)))
        if sources:
            sources = [src for src in sources if src]
        self.sources = sources if sources else None

        # Check for temp_dir
        assert_type(temp_dir, str)
        self.temp_dir = temp_dir

        # Check for visible_path, filter empty paths
        assert_type(visible_paths, (list, type(None)))
        if visible_paths:
            visible_paths = [path for path in visible_paths if path]
        self.visible_paths = visible_paths if visible_paths else None

        # Check for run_opts
        assert_type(run_opts, str)
        self.run_opts = run_opts

        # Check for copy_dir
        assert_type(copy_dir, str)
        self.copy_dir = copy_dir

        # Check for debug
        assert_type(debug, str)
        self.debug = debug

        # Check for runner
        assert_type(runner, str)
        if runner not in [BATS, BASH]:
            raise Exception(f'Unknown test runner, must be "{BATS}" or "{BASH}"')
        self.runner = runner.lower()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
