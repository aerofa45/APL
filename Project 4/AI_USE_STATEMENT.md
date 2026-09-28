# AI Use Statement - Project Part 4

OpenAI Codex assisted with the Part 4 interpreter, environment module, test
programs, expected outputs, automated tests, documentation, and packaging.
The existing Parts 1-3 implementation supplied the lexer, grammar, parser, and
AST interface. The AI assistant inspected those files before implementing Part 4.

## Concrete suggestion corrected and verified

A candidate shortcut was to let Python's numeric type behavior define Emerald
arithmetic, using `isinstance(value, (int, float))`. This was rejected because
Python bool inherits from int: that check accepts True and would allow
`true + 1` to produce 2. The implementation instead uses
`type(value) in (int, float)`, keeping Emerald booleans separate from numbers.

Verification includes the `print(true+1);` case in
`test_interpreter.py::InterpreterTests.test_runtime_error_cases` and
`error_programs/error_invalid.em`. The required result is a numeric-operand
runtime error, not 2. Boolean array indexes and mixed boolean/numeric equality
are also rejected and tested. This verification was performed by the AI
assistant using the actual test runner; it is not a claim of student review.

The assistant also tested lexical scoping with a function called from a scope
that shadows a global variable. Its output must come from the defining scope,
not the caller's scope. Expected example outputs were specified separately
from the actual output captured by the interpreter.

## Group review still required

Before submission, group members should run the tests themselves, examine the
code and the correction above, and record who reviewed or modified which parts
in CONTRIBUTIONS.md. Do not claim a group member performed work or verification
that they have not performed. This statement discloses substantial generated
code; it does not describe the implementation as independently student-written.
