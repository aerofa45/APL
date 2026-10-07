# Individual Contributions

## Group Record Carried from GitHub

### Abir

• Reviewed how the new keywords get to be tokens and AST nodes. Verified semicolons and source locations.
• Added code extensions in `token_definitions.py`, `lexer.py`, `ast_nodes.py`, `emerald_parser.py`, `ast_diagram.py`, and `GRAMMAR.md`.
• Tested `18_precedence.em` both with and without the AST diagram for the parser demonstration.
• Built `ast_nodes.py`, `emerald_parser.py`, and `ast_diagram.py`.
• Verified and demonstrated expression parsing, AST construction, and operator precedence.

### Md Shohag Ali Sarder

• Reviewed and verified the lexical-analysis stage of Emerald.
• Worked with `lexer.py` and `token_definitions.py` to understand and verify how source text gets converted into tokens.
• Tested the lexer using `18_precedence.em`.
• Verified recognition of keywords, identifiers, numbers, operators, parentheses, and statement terminators.
• Reviewed how source positions get attached to tokens so that later stages can give useful error locations.
• Prepared the lexer demonstration showing the Emerald source program together with its generated tokens.
• Reviewed the connection between source-code text and the token stream used by the parser.

### Prashant

• Reviewed and verified the array implementation and loop-control features in `interpreter.py`.
• Reviewed array access and validation, including integer-index checking and array-bounds checking.
• Tested the array examples in `07_functions_arrays.em` and `17_function_arrays.em`.
• Reviewed and verified the `break` and `continue` extensions.
• Tested `14_for_continue.em`, `15_while_break.em`, and the nested-loop behavior in `16_nested_loops.em`.
• Reviewed how `BreakSignal` and `ContinueSignal` get generated and handled by the interpreter.
• Verified that `break` exits the current loop while `continue` skips the remainder of the current iteration.
• Reviewed error handling for lexical and syntax errors.
• Tested `error_lexical.em` and `error_syntax.em` and verified that Emerald reports meaningful error messages.
• Reviewed the relevant error-handling path in `interpreter.py`.
• Prepared demonstration evidence and screenshots for arrays, `break`, `continue`, lexical errors, and syntax errors.

### Aman

• Reviewed and demonstrated the overall Emerald architecture: source program → lexer → tokens → parser → AST → interpreter → output.
• Added six Part 5 demonstration programs: `09_function_add.em`, `10_global_local_scope.em`, `11_local_lifetime.em`, `12_lexical_scope.em`, `13_recursive_factorial.em`, and `17_function_arrays.em`.
• Added the corresponding expected-output and captured actual-output files.
• Inherited the `test_interpreter.py` suite into Part 5.
• Committed these files to the Aman branch and merged them into `master`.
• Reviewed and demonstrated the main interpreter behavior for variables, arithmetic, comparisons, `if/else`, and `while` loops.
• Reviewed function execution in `interpreter.py`, including argument evaluation, creation of the function-call environment, parameter binding, execution of the function body, and return handling.
• Reviewed lexical scope and environment chaining in `environment.py`.
• Tested and demonstrated `09_function_add.em`, showing the function result `30`.
• Tested and demonstrated `10_global_local_scope.em`, showing that a local `x = 20` does not overwrite the global `x = 10`.
• Verified the architecture, function-execution, and scope portions of the final presentation.

### Toufique Hasan

• Reviewed the completed testing and verification process for the Part 6 package.
• Ran and reviewed the automated unit-test suite using `python -m unittest discover -v`.
• Ran and reviewed the example verification system using `verify_examples.py`.
• Verified that example-program outputs are compared with their expected-output files.
• Reviewed `test_extension.py` and the tests covering loop controls, invalid use of `break` and `continue`, nested loops, scope behavior, and related regression cases.
• Verified `AI_USE_STATEMENT.md` against the implemented code and the tests referenced by the documentation.
• Reviewed the loop-depth logic in `interpreter.py` and confirmed its behavior through tests.
• Reviewed the correction to AST-diagram handling for `break` and `continue`.
• Prepared the final testing evidence, test-summary screenshots, example-verification evidence, and AI-use explanation for the presentation.



These Codex-assisted package-preparation actions are not attributed to an individual student. The student contributions listed above represent their actual development work, subsequent review, testing, verification, documentation, and presentation responsibilities.
