# AI Use Statement - Project Part 4

## How our group used AI

Our group (Aman and Abir) wrote and owned the Part 4 interpreter. We used an AI
coding assistant (OpenAI Codex) as a support tool, not as a replacement for our
own work. We mainly used it to:

- explain concepts we were unsure about, such as how lexical scoping differs
  from dynamic scoping and how to implement `return` using an exception;
- review pieces of code we had already written and point out edge cases;
- suggest additional test cases and error programs;
- help clean up wording and formatting in our documentation.

The lexer, grammar, parser, and AST from Parts 1-3 were our own earlier work,
and Part 4 was built directly on top of that interface. Design decisions (how
environments are chained, what counts as a runtime error, how values are
printed) were made by our group.

## Components that received AI assistance

| Component                                                                    | Who led it | How AI helped                                                                  |
| ---------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------ |
| `interpreter.py` (`Interpreter`, `Function`, `ReturnSignal`, `format_value`) | Aman       | Explained the `ReturnSignal` pattern; reviewed type checks in arithmetic       |
| `environment.py` (scope chain)                                               | Group      | Explained lexical vs. caller scope; Shohag used AI for some code completion    |
| `programs/`, `error_programs/`, `expected/`                                  | Group      | Suggested extra edge cases (shadowing, zero-iteration loops, division by zero) |

| `test_interpreter.py`, `verify_examples.py`
NO AI was used as powershell verified the pass test

| `GRAMMAR.md`, `ARCHITECTURE.md`, `README.md` | Abir, Aman | Suggestions on proofreading and formatting |

## An AI suggestion we corrected

While performing the arithmetic validation, the AI made a proposal to use
`isinstance(value, (int, float))`, but we did not accept it. In Python, `bool`
is derived from `int`, and any call like `print(true + 1);` would yield `2`.
For us, booleans are not numbers, which should produce a runtime bug.

So we highlighted `type(value) in (int, float)` (see `Interpreter.number` and
`Interpreter.binary` methods in `interpreter.py`) to make a difference
between numbers and booleans. We then added `print(true+1);` to
`test_interpreter.py::InterpreterTests.test_runtime_error_cases` and to
`error_programs/error_invalid.em` and confirmed that it produces
a "numeric operand required" message instead of `2`. We applied
the same logic to array references, hence `a[true]` also fails.

In addition, we did not use AI output for our expected results. The data in the `expected/` directory was typed manually according to the Emerald rules about what it should output. After writing this data we verified it against the data produced by the interpreter which we stored in the `actual/` directory. Thanks to this approach, the interpreter bug could not pass unnoticed to the category of the "correct" answer.

## How we tested and verified AI-assisted work

- We ran `python -m unittest discover -v` in each part's directory. All Part 4
  tests pass (21 tests, including the parameterized error cases), and the
  Part 2 and Part 3 tests still pass.
- We ran `python verify_examples.py`, which runs every `.em` program through the
  interpreter and compares output and exit code with `expected/`. All 11
  programs match (8 normal programs exit 0; 3 error programs exit 1 with the
  expected message on stderr).
- We traced some programs by hand, for example `programs/06_scope.em`, to
  confirm that the inner `total` shadows the outer one and the outer value is
  printed afterwards.
- For lexical scoping, we wrote a test where a function is called from a scope
  that shadows a global variable, and checked that the function uses the
  variable from where it was defined, not where it was called
  (`test_lexical_scope_not_caller_scope`).
- Any AI explanation we used, we checked against lecture notes and by running
  small examples before putting it in the code.

## What we learned

- AI is useful for explaining ideas and suggesting edge cases, but its code
  can look correct while hiding subtle bugs, like the `bool`/`int` problem.
  We discovered that we must comprehend both the language we are working with and the language we are applying it through.
- Writing a specification of anticipated outputs is extremely beneficial in detecting errors that may not be discerned by running tests based on the actual result produced by the program.
- The AI's ability to tell us what we neglected to consider proved far more useful than its ability to produce code because it made us think through the work.
- Any suggestion made by the AI must be accompanied by a test. If the test written proves that the suggestion provided is incorrect, it cannot be used by us.
