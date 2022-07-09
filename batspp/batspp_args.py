#!/usr/bin/env python3
#
# Batspp arguments module
#


"""Batspp arguments module"""


class BatsppArgs:
    """Batspp test related arguments"""

    def __init__(self,
                 sources: (list|None) = None,
                 temp_dir: str = '',
                 visible_paths: (list|None) = None,
                 run_opts: str = '',
                 copy_dir: str = '') -> None:
        __error_string = 'invalid type'

        # Check for sources, filter empty sources
        assert isinstance(sources, (list|None)), __error_string
        if sources:
            sources = [src for src in sources if src]
        self.sources = sources if sources else None

        # Check for temp_dir
        assert isinstance(temp_dir, str), __error_string
        self.temp_dir = temp_dir

        # Check for visible_path, filter empty paths
        assert isinstance(visible_paths, (list|None)), __error_string
        if visible_paths:
            visible_paths = [path for path in visible_paths if path]
        self.visible_paths = visible_paths if visible_paths else None

        # Check for run_opts
        assert isinstance(run_opts, str), __error_string
        self.run_opts = run_opts

        # Check for copy_dir
        assert isinstance(copy_dir, str), __error_string
        self.copy_dir = copy_dir
