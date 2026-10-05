# Emerald Interpreter - Project Part 4

Emerald now executes the AST produced by Part 3. Requires Python 3.10 or later;
the interpreter and tests use only the standard library.

## Run

From `Project_part_4`:

```sh
python interpreter.py programs/05_while.em
python -m unittest discover -v
python verify_examples.py
```

The example prints 1 through 5, each on its own line. Successful execution exits
with status 0. Lexical, syntax, file, and runtime errors exit with status 1;
command-line usage errors exit with status 2. Interpreter errors go to stderr;
program output goes to stdout. Execution stops at the first error; earlier
printed output is retained.

An execution budget defaults to 100,000 AST visits to stop accidental infinite
loops. Increase it for larger programs:

```sh
python interpreter.py programs/05_while.em --max-steps 1000000
```

## Files and submission contents

- `lexer.py`, `token_definitions.py`: unchanged Part 2 scanner.
- `emerald_parser.py`, `ast_nodes.py`, `ast_diagram.py`: unchanged Part 3 parser and trees.
- `environment.py`: nested dictionaries, declarations, lookup, assignment, runtime error type.
- `interpreter.py`: AST execution, expression evaluation, functions, arrays, CLI.
- `test_interpreter.py`: automated behavioral tests, including rejection cases.
- `programs/`: eight complete successful programs.
- `error_programs/`: three complete programs demonstrating required runtime errors.
- `expected/`: independently specified expected output.
- `actual/`: captured interpreter output, produced by `verify_examples.py`.
- `verify_examples.py`: checks output, error streams, and exit codes against expectations.
- `GRAMMAR.md`: grammar and Part 4 runtime semantics.
- `ARCHITECTURE.md`: implementation explanation and source walkthrough.
- `AI_USE_STATEMENT.md`: assistance disclosure and verified correction.
- `CONTRIBUTIONS.md`: honest contribution-recording guidance.

The complete submission ZIP includes Parts 1-4. Part 4 also runs independently.
The earlier parts are retained as historical milestones, including their own tests.

## Implemented behavior

Variables, assignment, numeric arithmetic, all six comparisons, printing,
if/else, while, logical operators, block scope, for loops, functions, recursion,
and arrays execute. The parser establishes precedence; the interpreter follows
the tree. No host-language `eval` or `exec` is used.

Values are integers, finite decimal numbers, booleans, arrays, functions, or the
internal no-result value printed as `nil`. Division is real division (`9/2` is
`4.5`, `8/2` is `4.0`). Arithmetic and ordering require numbers; booleans are not
numbers. Equality permits two numbers or two booleans. Conditions require booleans.
`and` and `or` short-circuit. Variables are dynamically typed.

`let` declares in the current scope and rejects duplicates there. Inner scopes
may shadow outer names. Assignment requires an existing declaration and updates
the closest matching scope. Blocks create scopes; each loop iteration has a fresh
body scope. A for-loop initializer has its own scope. Functions capture their
defining environment, not their caller's environment. Declarations execute in
order and are not hoisted. Parameters and the function's top-level body share a
scope. A bare return or falling off a function produces `nil`.

Arrays use zero-based integer indexes with bounds checks. Assignment shares an
array reference, so mutations through an alias are visible. Negative indexes,
boolean indexes, array arithmetic, and array equality are rejected. There is no
`length` builtin, string syntax, chained indexing, or `else if` syntax; these are
not in the inherited language grammar. Pass an array's count explicitly.

## Rubric evidence

| Criterion | Evidence |
|---|---|
| Expressions and variables | programs 01-02; expression and environment tests |
| If/else | program 04 covers both branches |
| While | program 05 counts 1-5; program 06 accumulates squares |
| Environment/symbol table | environment.py; program 06; lexical scope tests |
| Runtime errors | error_programs; negative automated cases with locations |
| Testing | eight success programs, three error programs, expected/actual files |
| Code quality | separate scanner, parser, AST, environment, interpreter modules |
| AI use | AI_USE_STATEMENT.md with correction and regression evidence |
| GitHub/individual work | CONTRIBUTIONS.md; actual commits and member review required |


