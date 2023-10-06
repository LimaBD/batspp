#!/usr/bin/env python3
#
# Timer module
#

"""
Timer module

This provide useful tools to measure time.
"""

# Standard packages
import time

class Timer:
    """Timer class used for
       debugging and profiling"""

    def __init__(self) -> None:
        """Initialize the timer"""
        self.start_time = None
        self.end_time = None

    def start(self) -> None:
        """Start the timer"""
        self.start_time = time.time()
        self.end_time = None

    def stop(self) -> None:
        """Stop the timer"""
        self.end_time = time.time()
        return self.end_time - self.start_time
