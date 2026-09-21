# AI Use Statement

Claude Code (Claude Sonnet 5, Anthropic) was used to read the supplied Part 1
Emerald language document, the Part 2 lexer and the Part 3 task description,
generate the recursive-descent parser and AST node classes, create automated
tests and documentation, run verification, save example outputs, and package
the project.

The parser builds directly on the Part 2 lexer, which was reused without
changes. Claude Code followed the Part 1 grammar exactly, including its
operator precedence, its letter-first identifier rule and its `if`/`else`
form. The original Part 1 document was provided as the language specification.

### AI USE STATEMENT

**AI Tool(s) Used:**

Claude Code (Claude Sonnet 5), running in VS Code.

**How did your group use AI for this project milestone?**

Our group used AI to help implement the Emerald parser based on our Part 1 grammar and the Part 2 lexer. AI helped generate and explain Python code, design the AST node classes, suggest test cases, and prepare documentation and running instructions.

**Which project components received AI assistance?**

AI assisted with `emerald_parser.py`, `ast_nodes.py`, `test_parser.py`, `generate_outputs.py`, the example programs in `test_inputs/`, the saved outputs in `outputs/`, the README, `GRAMMAR.md` and the written report. The Part 2 lexer and token definitions were not changed.

**Describe at least one AI-generated suggestion, explanation, or code segment that your group modified, corrected, rejected, or improved.**

Our group corrected the AI's first test helper, which wrapped every expression as `let _ = ...;`. The lexer rejected it with "invalid character '_'", because Part 1 requires identifiers to start with a letter. The helper now uses `let v = ...;`. The test was wrong, not the lexer, so the lexer was left alone to keep Part 2 intact.

We also renamed the AI's first node classes (Program, Number, Identifier, Assign) to ProgramNode, NumberNode, VariableNode and AssignmentNode to follow the Part 3 task. We deleted two copied Part 2 lexer tests that failed in the Part 3 folder because they depend on Part 2's layout. We kept the parser strict to the Part 1 grammar rather than allowing extras such as `else if` or `a[0][1]`, which are reported as syntax errors.

**How did your group test or independently verify AI-assisted work?**

We ran the parser on ten example programs (six valid, four invalid) and checked the tree printed for each. The valid programs exit with status 0 and the invalid ones with status 1. Claude Code also ran 52 automated parser tests, which all passed, including checks that `2 + 3 * 4` builds the tree with `*` below `+` and that `let x = ;` is reported at line 1, column 9. We compared `lexer.py` and `token_definitions.py` with the Part 2 files and confirmed they are identical, and Part 2's 17 tests still pass. The parser's rules were also compared one by one with the Part 1 BNF/EBNF.

**What did your group learn from using AI during this milestone?**

We learned how a recursive-descent parser turns a token stream into an abstract syntax tree, and how operator precedence comes from the order of the parsing methods, with one method per level and tighter operators parsed deeper. We learned that an assignment target is only known after the whole left side has been parsed. We also learned that a generated test can fail because the test is wrong, not the code, so each failure has to be checked against the grammar before anything is changed.

**The purpose of this statement is to document how AI contributed to your development process and how your group evaluated its output.**
