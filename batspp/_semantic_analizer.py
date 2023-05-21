#!/usr/bin/env python3
#
# Semantic Analizer module
#
# This is responsible for the semantic analisis of the AST tree

"""
Semantic Analizer module

This is responsible for the semantic analisis of the AST tree
"""

# Standard packages
## NOTE: this is empty for now

# Installed packages
from mezcla import debug

# Local packages
from batspp._exceptions import (
    warning_not_intended_for_cmd,
    )
from batspp._ast_node import (
    ASTnode,
    )

class _SemanticAnalizer:
    """Semantic analizer class"""

    def __init__(self) -> None:
        """Initialize the class"""
        pass

    def analize(self, tree: ASTnode) -> None:
        """Analize the semantic of the code"""
        ## TODO: error if any setup if after the test that is referenced.
        ## TODO: check if any setup has wrong reference (no test with that reference).
        ## TODO: handle multiple setup with same referece (by adding a number to the reference).
        ## TODO: handle external configuration (from command line opts and args).
        return tree

semantic_analizer = _SemanticAnalizer()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
