#!/usr/bin/env python3
#
# Node visitor module
#

"""
Node visitor module
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
    TestReference, SetupReference,
    ASTnode,
    )

class NodeVisitor:
    """Implements a generic method visit"""

    def visit(self, node):
        """Generic method to visit NODE"""
        if node is None:
            raise Exception("Node to visit can't be None")
        if not isinstance(node, ASTnode):
            raise Exception(f"Node to visit must be a ASTnode, not a {type(node).__name__}")
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visitor)
        debug.trace(7, f'NodeVisitor.visitor({node}) => {method_name}({node})')
        return visitor(node)

    def visit_optional(self, node, default=None):
        """Generic method to visit optional NODE"""
        if node is None:
            return default
        return self.visit(node)

    def generic_visitor(self, node) -> None:
        """Raise exception if the visit method to NODE not exist"""
        raise Exception(f'No visit_{type(node).__name__} method founded')

class ReferenceNodeVisitor(NodeVisitor):
    """Wrapper for NodeVisitor to visit a references"""

    # pylint: disable=invalid-name
    def visit_TestReference(self, node: TestReference) -> str:
        """
        Visit TestReference NODE
        """
        return node.reference.value.strip()

    # pylint: disable=invalid-name
    def visit_SetupReference(self, node: SetupReference) -> str:
        """
        Visit TestReference NODE
        """
        return node.reference.value.strip()

if __name__ == '__main__':
    warning_not_intended_for_cmd()
