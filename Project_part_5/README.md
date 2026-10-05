Emerald — Part 5: Functions, Scope, and Extension
Requires Python 3.10+; execution and tests only use the standard library.

Run
From Project_part_5: python interpreter.py programs/09_function_add.em python -m unittest discover -v python verify_examples.py

Expected output of the first command is 30. Emerald uses func, not the illustrative function keyword in the assignment. Definitions, parameters, calls, return values and function-local variables are supported.

Scope
Environment holds a values dictionary and a parent link. A function captures its defining environment. A call binds parameters in a new child environment. Local declarations shadow globals, without changing them. Assignment updates the nearest existing binding. A local name cannot be accessed after its call finishes. Blocks create child scopes; parameters and the function body share a call scope.

New extension
Part 5 adds break and continue. Break exits the nearest current-function loop. Continue skips the remaining body, but for updates still execute. A called function cannot use either statement to control its caller's loop. Arrays, for loops, recursion, closures, and comments are still supported from Part 4.

Files
interpreter.py: function execution, values, returns, loops, and extension. environment.py: global/local scope representation and lookup. ast_nodes.py: complete AST including new BreakNode and ContinueNode. lexer.py and token_definitions.py: scanner including the new keywords. emerald_parser.py: complete parser including semicolon-terminated loop controls. GRAMMAR.md: full EBNF and runtime rules. ARCHITECTURE.md: diagrams and implementation explanation. programs/: 17 success programs, including nine new assignment-focused programs 09–17. error_programs/: three runtime-error programs. expected/: specified output; actual/: output from the verified run. test_interpreter.py and test_extension.py: behavioral and regression checks. verify_examples.py: exact output, stream, and exit-code verification. AI_USE_STATEMENT.md: truthful disclosure of assistance in this submission. TEST_RESULTS.md: results of the current verification run.

New program coverage
09: definitions, two parameters, call, return, local sum. 10: required global/local shadowing example (20 then 10). 11: independent call locals. 12: lexical scope rather than caller scope. 13: recursive factorial. 14: for loop with continue and return. 15: while loop with break. 16: nearest-loop break in nested loops. 17: array parameter and for-loop accumulation. The automated negative tests also demonstrate that locals cannot escape a call.

Limits
No strings, user input, length builtin, direct else if, or chained indexing. Conditions must be booleans, booleans are not numeric operands. Errors include source locations and stop execution. A default 100,000 AST-visit budget limits accidental infinite loops. This is not a security sandbox.
