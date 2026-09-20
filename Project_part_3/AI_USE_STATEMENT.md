# AI Use Statement (Project Part 3)

**AI tool used:** Claude Code (Claude Sonnet 5, Anthropic), running in VS Code.

**How AI was used:** The AI read the Part 1 grammar, the Part 2 lexer and the
Part 3 task description, and it generated the parser, the AST node classes,
the unit tests, the example programs, the saved outputs, the README, the
grammar document and the written report. It ran the tests and the command-line
tool to check its own work.

**Components that received AI assistance:** emerald_parser.py, ast_nodes.py,
test_parser.py, generate_outputs.py, the files in test_inputs/, the files in
outputs/, README.md, GRAMMAR.md and the report. The Part 2 lexer was not
changed; it was copied as it was submitted for Part 2.

**AI suggestions that were corrected, modified or rejected:**

1. Corrected. The AI's first test helper wrapped every expression as
   `let _ = ...;`. The lexer rejected it with "invalid character '_'", because
   Part 1 says identifiers must start with a letter. Running the tests exposed
   the mistake, and the helper now uses `let v = ...;`. The test was wrong, not
   the lexer, so the lexer was left alone to keep Part 2 intact.
2. Modified. The AI first named the nodes Program, Number, Identifier and
   Assign. The Part 3 task suggests ProgramNode, NumberNode, VariableNode,
   AssignmentNode and so on, so all nodes were renamed to that convention.
3. Rejected. The AI copied the Part 2 lexer tests into the Part 3 folder, and
   two of them failed because they depend on Part 2's layout. They were
   deleted, since they are Part 2 tests and still pass in Part 2's folder.
4. Kept as specified. The AI could have made the parser more permissive (for
   example, allowing `else if` or `a[0][1]`). It follows the Part 1 grammar
   exactly instead, and both cases are reported as syntax errors.

**How the AI's work was verified:**

- 52 automated parser tests pass, including checks that `2 + 3 * 4` builds
  the tree with `*` below `+`, and that `let x = ;` is reported at line 1,
  column 9.
- The parser was run on ten example programs (six valid, four invalid). The
  valid ones exit with status 0 and the invalid ones with status 1.
- `lexer.py` and `token_definitions.py` were compared with the Part 2 files
  and are identical, and Part 2's 17 tests still pass.
- The grammar in the parser was compared rule by rule with the Part 1
  BNF/EBNF.

**What was learned:** Operator precedence can come from the order of the
parsing methods, with one method per level and tighter operators parsed
deeper. An assignment target is only known after the whole left side has been
parsed. A generated test can fail because the test is wrong, not the code, and
each failure has to be checked against the grammar before anything is changed.
