# Emerald - Final Project (Part 6)

Emerald is an educational programming language implemented in Python.
Requires Python 3.10+. No external packages are needed to run or test it.

## Quick start
Extract the ZIP and open a terminal inside YourLanguage.
~~~bash
python main.py tests/programs/09_function_add.em
python -m unittest discover -v
python verify_examples.py
~~~
The first command prints 30. Verification covers 18 successful programs and
five intentional error programs. Run tests from the project root.

## Demonstrate the pipeline
~~~bash
python lexer.py tests/programs/18_precedence.em
python parser.py tests/programs/18_precedence.em
python parser.py tests/programs/18_precedence.em --diagram
python main.py tests/programs/18_precedence.em
~~~
Execution prints 14 then 20. The AST groups multiplication inside addition.

## Functions
Emerald uses func, not function:
~~~text
func add(a, b) {
    let result = a + b;
    return result;
}
print(add(10, 20));
~~~
Variables/assignment, arithmetic, precedence, six comparisons, printing,
if/else, while, functions, parameters/returns, global/local scope and arrays
are supported. Extensions include for loops, recursion, break and continue.
Arithmetic excludes booleans. Conditions require booleans. Division is real
division; logical and/or short-circuit.

## Scope
An Environment has a values dictionary and a parent link. Declarations create
local bindings; assignment updates the nearest existing one. Functions capture
their defining environment. Calls create child environments and bind parameters.
Parameters and the function body share a scope. Nested blocks create child scopes.
Returned closures can retain their defining local environment. Local names are
not directly accessible outside their lexical scope. Bare/implicit return yields
an internal value displayed as nil.

## Extensions
Break exits the nearest loop in the current function. Continue skips the remaining
body, and for updates still run. Called functions cannot control caller loops.
Arrays use checked zero-based integer indexes and shared-reference semantics.

## Errors
~~~bash
python main.py tests/error_programs/error_lexical.em
python main.py tests/error_programs/error_syntax.em
python main.py tests/error_programs/error_undefined.em
python main.py tests/error_programs/error_division.em
python main.py tests/error_programs/error_invalid.em
~~~
These intentionally exit 1 and report on stderr. Success exits 0 and writes
program output to stdout. CLI usage errors exit 2. Execution stops at the first
error. Earlier runtime output is retained; syntax errors prevent execution.

## Files
- main.py: primary entry point.
- lexer.py, token_definitions.py: source to positioned tokens.
- parser.py: recursive-descent parser.
- ast_nodes.py, ast_diagram.py: AST definitions and diagrams.
- interpreter.py: statement execution and expression evaluation.
- environment.py: linked dictionaries and runtime error type.
- tests/: unit tests, success/error programs, expected/actual outputs.
- verify_examples.py: exact output, streams, exit codes and fixture checks.
- GRAMMAR.md, ARCHITECTURE.md: language rules and implementation.
- CONTRIBUTIONS.md, AI_USE_STATEMENT.md: contribution and assistance records.
- CHANGELOG_PART6.md, TEST_RESULTS.md: changes and verification.

## Limits
No strings, user input, length builtin, direct else if or chained indexing.
The default execution budget is 100,000 AST visits, not a security sandbox.
~~~bash
python main.py tests/programs/05_while.em --max-steps 1000000
~~~


