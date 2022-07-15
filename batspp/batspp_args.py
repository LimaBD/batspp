#!/usr/bin/env python3
#
# Batspp arguments module
#


"""Batspp arguments module"""


# Local modules
from exceptions import assert_type


class BatsppArgs:
    """Batspp test related arguments"""

    def __init__(self,
                 sources: 'list|None' = None,
                 temp_dir: str = '',
                 visible_paths: 'list|None' = None,
                 run_opts: str = '',
                 copy_dir: str = '') -> None:

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
