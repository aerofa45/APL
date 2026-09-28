"""AST node definitions for Emerald.

Every node records the line and column of the token that starts it. Those
positions are excluded from equality so tests can compare tree shapes only.
"""
from dataclasses import dataclass, field, fields
from typing import Optional, Union


@dataclass
class Node:
    line: int = field(default=0, compare=False, repr=False, kw_only=True)
    column: int = field(default=0, compare=False, repr=False, kw_only=True)


# ----- Expressions -------------------------------------------------------

@dataclass
class NumberNode(Node):
    value: Union[int, float]


@dataclass
class BooleanNode(Node):
    value: bool


@dataclass
class VariableNode(Node):
    name: str


@dataclass
class ArrayNode(Node):
    elements: list


@dataclass
class IndexNode(Node):
    name: str
    index: Node


@dataclass
class CallNode(Node):
    name: str
    arguments: list


@dataclass
class UnaryOpNode(Node):
    operator: str
    operand: Node


@dataclass
class BinaryOpNode(Node):
    operator: str
    left: Node
    right: Node


# ----- Statements --------------------------------------------------------

@dataclass
class ProgramNode(Node):
    statements: list


@dataclass
class BlockNode(Node):
    statements: list


@dataclass
class DeclarationNode(Node):
    """`let name = value;`"""
    name: str
    value: Node


@dataclass
class AssignmentNode(Node):
    """`target = value;` where target is a VariableNode or IndexNode."""
    target: Node
    value: Node


@dataclass
class PrintNode(Node):
    value: Node


@dataclass
class IfNode(Node):
    condition: Node
    then_branch: BlockNode
    else_branch: Optional[BlockNode] = None


@dataclass
class WhileNode(Node):
    condition: Node
    body: BlockNode


@dataclass
class ForNode(Node):
    init: Node  # DeclarationNode or AssignmentNode
    condition: Node
    update: AssignmentNode
    body: BlockNode


@dataclass
class FunctionNode(Node):
    name: str
    parameters: list  # list of parameter names
    body: BlockNode


@dataclass
class ReturnNode(Node):
    value: Optional[Node] = None


@dataclass
class ExpressionStatementNode(Node):
    expression: Node


def format_tree(node, label=None, depth=0):
    """Return an indented, human-readable rendering of an AST."""
    pad = "  " * depth
    scalars = []
    children = []
    for f in fields(node):
        if f.name in ("line", "column"):
            continue
        value = getattr(node, f.name)
        if isinstance(value, Node):
            children.append((f.name, value))
        elif isinstance(value, list) and value and isinstance(value[0], Node):
            children.extend((f"{f.name}[{i}]", item) for i, item in enumerate(value))
        elif value is not None:
            scalars.append(f"{f.name}={value!r}")

    header = f"{label}: " if label else ""
    header += type(node).__name__
    if scalars:
        header += " " + " ".join(scalars)
    lines = [f"{pad}{header}"]
    for child_label, child in children:
        lines.append(format_tree(child, child_label, depth + 1))
    return "\n".join(lines)
