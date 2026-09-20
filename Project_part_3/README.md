# Emerald Parser (Project Part 3)

## Description

This project implements a parser for the Emerald programming language
designed in Part 1. It reads the token stream produced by the Part 2 lexer
and builds an abstract syntax tree (AST) using recursive descent. For example,
`2 + 3 * 4` becomes a BinaryOpNode for `+` whose right child is a BinaryOpNode
for `*`, so multiplication is evaluated first.

The parser checks syntax only. It does not execute programs, check scopes or
types, or check array bounds.

## Relationship to Parts 1 and 2

- The grammar is the Part 1 BNF/EBNF, unchanged (see GRAMMAR.md).
- `lexer.py` and `token_definitions.py` are the Part 2 files, copied without
  changes so that this folder runs on its own. Part 2's own 17 tests still pass.
- Nothing in Part 1 or Part 2 was modified.

## Requirements

- Python 3.10 or later
- No external packages are required

## Running the Parser

From this directory, run:

```sh
python emerald_parser.py test_inputs/test1_precedence.em
```

Replace the filename with any Emerald source file. On success the AST is
printed as an indented tree and the exit status is 0. Lexical and syntax
errors print a message with line and column and exit with status 1.

Example error (`test_inputs/test7_invalid_missing_expression.em` contains
`let x = ;`):

```
Syntax error at line 1, column 9: expected expression, found ';'
```

## Running the Tests

```sh
python -m unittest discover -v
```

## Files

- emerald_parser.py: Recursive-descent parser and command-line entry point
- ast_nodes.py: AST node classes and the tree printer
- lexer.py, token_definitions.py: The Part 2 lexer, unchanged
- test_parser.py: 52 automated tests (AST shape, precedence, errors, CLI)
- test_inputs/: Emerald programs (test1 to test6 are valid, test7 to test10 have syntax errors)
- outputs/: Saved parser output for every test input
- generate_outputs.py: Regenerates outputs/ by running the CLI on each input
- GRAMMAR.md: The grammar, the rule to node mapping, and parsing decisions
- AI_USE_STATEMENT.md: How AI was used and how its output was checked
- Project_Part_3_Report.docx: The written report

## AST design

Each node is a small dataclass. The required node types are ProgramNode,
NumberNode, VariableNode, BinaryOpNode, AssignmentNode and PrintNode. The
rest of the Part 1 grammar adds DeclarationNode (`let`), UnaryOpNode,
BooleanNode, BlockNode, IfNode, WhileNode, ForNode, FunctionNode, ReturnNode,
CallNode, ArrayNode, IndexNode and ExpressionStatementNode. Every node records
the line and column of its first token (the operator's position for
BinaryOpNode). Positions are ignored when trees are compared, so tests compare
shape only.

## Error handling

The parser stops at the first error rather than trying to recover, as the
lexer does. Messages have the form
`Syntax error at line L, column C: expected <what>, found <token>`.

## Test coverage

`test_parser.py` covers every statement form, every operator level,
associativity, unary operators, arrays and indexing, calls, node positions,
about twenty kinds of syntax error with their line and column, lexical errors
passing through the parser, and the command-line behavior on all example
files. Saved outputs come from running the CLI on each input. The four invalid
inputs exit with status 1 on purpose.

| Input | Shows |
|---|---|
| test1_precedence.em | `2 + 3 * 4` and `(2 + 3) * 4` |
| test2_variables_assignment.em | Variables, assignment, multiple statements, print |
| test3_control_flow.em | if/else and while |
| test4_for_loop.em | for loops |
| test5_functions.em | Functions, parameters, return |
| test6_arrays.em | Array literals and indexing |
| test7 to test10 (invalid) | Missing expression, missing semicolon, invalid assignment target, unclosed block |
