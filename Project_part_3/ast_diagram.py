"""Draw an Emerald AST as a text diagram, for example:

     +
    / \\
   2   *
      / \\
     3   4

Each node is shown by a short label (an operator, a number, a variable name,
or a keyword). Children hang below their parent, joined by / | \\ lines.
"""
from dataclasses import fields

import ast_nodes as ast

MAX_WIDTH = 100  # wider diagrams are not drawn; the caller falls back to text
SLASH_LIMIT = 3  # up to this many columns from parent to child, draw / \ lines


def label(node):
    """Short text shown for a node in the diagram."""
    if isinstance(node, ast.NumberNode):
        return str(node.value)
    if isinstance(node, ast.BooleanNode):
        return "true" if node.value else "false"
    if isinstance(node, ast.VariableNode):
        return node.name
    if isinstance(node, (ast.BinaryOpNode, ast.UnaryOpNode)):
        return node.operator
    if isinstance(node, ast.IndexNode):
        return f"{node.name}[ ]"
    if isinstance(node, ast.CallNode):
        return f"{node.name}( )"
    if isinstance(node, ast.ArrayNode):
        return "[ ]"
    if isinstance(node, ast.DeclarationNode):
        return f"let {node.name}"
    if isinstance(node, ast.AssignmentNode):
        return "="
    if isinstance(node, ast.FunctionNode):
        return f"func {node.name}({', '.join(node.parameters)})"
    names = {
        ast.ProgramNode: "Program", ast.BlockNode: "{ }", ast.PrintNode: "print",
        ast.IfNode: "if", ast.WhileNode: "while", ast.ForNode: "for",
        ast.ReturnNode: "return", ast.ExpressionStatementNode: "expr",
    }
    return names[type(node)]


def children(node):
    """Child nodes in source order (positions and plain values excluded)."""
    result = []
    for f in fields(node):
        value = getattr(node, f.name)
        if isinstance(value, ast.Node):
            result.append(value)
        elif isinstance(value, list):
            result.extend(v for v in value if isinstance(v, ast.Node))
    return result


def _layout(node):
    """Return (lines, root_column) for the subtree rooted at node."""
    text = label(node)
    kids = [_layout(child) for child in children(node)]
    if not kids:
        return [text], (len(text) - 1) // 2

    # Place the children side by side. Two-child parents get an even distance
    # between the child roots so the two branches are symmetric.
    offsets = []
    x = 0
    for i, (lines, root) in enumerate(kids):
        if i:
            prev_lines, prev_root = kids[i - 1]
            leaves = len(prev_lines) == 1 and len(lines) == 1
            gap = 1 if leaves else 2
            x = offsets[-1] + max(len(l) for l in prev_lines) + gap
            if len(kids) == 2 and (x + root - (offsets[0] + kids[0][1])) % 2:
                x += 1
        offsets.append(x)
    roots = [offsets[i] + kids[i][1] for i in range(len(kids))]
    parent = (roots[0] + roots[-1]) // 2

    spread = max(abs(r - parent) for r in roots)
    connectors = []
    if spread <= SLASH_LIMIT:
        # Narrow: a branch moves one column per row toward its child.
        for row in range(1, max(spread, 1) + 1):
            cells = {}
            for r in roots:
                dx = r - parent
                if dx == 0:
                    cells[parent] = "|"
                elif row <= abs(dx):
                    cells[parent + (1 if dx > 0 else -1) * row] = "\\" if dx > 0 else "/"
                else:
                    cells[r] = "|"
            connectors.append(cells)
    else:
        # Wide: drop from the parent, run a bar across, drop to each child.
        bar = {col: "_" for col in range(min(roots), max(roots) + 1)}
        bar[parent] = "|"
        connectors.append(bar)
        connectors.append({r: "|" for r in roots})

    height = max(len(lines) for lines, _ in kids)
    rows = [{} for _ in range(height)]
    for (lines, _), off in zip(kids, offsets):
        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                if ch != " ":
                    rows[i][off + j] = ch

    # A label wider than the space to its left pushes the whole block right.
    start = parent - (len(text) - 1) // 2
    shift = max(0, -start)
    grid = [{start + shift + i: ch for i, ch in enumerate(text)}]
    grid += [{col + shift: ch for col, ch in row.items()} for row in connectors + rows]
    width = max((max(row) + 1 if row else 0) for row in grid)
    lines = ["".join(row.get(c, " ") for c in range(width)).rstrip() for row in grid]
    return lines, parent + shift


def draw(node):
    """Return the text diagram for a node, or None if it is too wide."""
    lines, _ = _layout(node)
    if max(len(l) for l in lines) > MAX_WIDTH:
        return None
    return "\n".join(lines)


def format_program_diagram(program):
    """Diagram each top-level statement separately, with a short heading."""
    from ast_nodes import format_tree

    parts = []
    for number, statement in enumerate(program.statements, 1):
        heading = f"Statement {number} (line {statement.line}):"
        drawing = draw(statement)
        if drawing is None:
            drawing = ("(too wide to draw as a diagram; indented tree shown instead)\n"
                       + format_tree(statement))
        parts.append(heading + "\n" + drawing)
    return "\n\n".join(parts) if parts else "(empty program)"
