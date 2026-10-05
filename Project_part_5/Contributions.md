Abir:

- Reviewed how the new keywords become tokens and AST nodes. Verified semicolons and source locations.
- Add code extension on these files - token_definitions.py, lexer.py, ast_nodes.py, emerald_parser.py, ast_diagram.py GRAMMAR.md

Prashant:

- Added changes to interpreter.py, environment.py, ARCHITECTURE.md
- Review function execution, scope dictionaries, and loop controls.

Aman:

- Added six part 5 demo programs to run: 09_function_add, 10_global_local_scope, 11_local_lifetime, 12_lexical_scope, 13_recursive_factorial, and 17_function_arrays.
- Added corresponding expected and captured actual output files.
- Inherited the test_interpreter.py suite into part 5.
- Committed these files on the Aman branch and merged into master.

Toufique Hasan:

- Verified AI_USE_STATEMENT.md against interpreter.py and the tests it names.
- Reviewed the loop-depth logic in interpreter.py and ran the unit tests and example programs.
