# Part 4 architecture and code walkthrough

## 1. Execution pipeline

```text
Emerald .em source
       |
       v
Lexer.tokenize()       characters -> tokens with line/column
       |
       v
Parser.parse()         tokens -> ProgramNode and child AST nodes
       |
       v
Interpreter.execute()  statements -> state changes / output / control flow
       |
       +--> evaluate() expressions -> values
       +--> Environment dictionaries -> variables and functions
       +--> output stream -> print results
```

The interpreter imports `parse_source` from the unchanged Part 3 parser.
`run()` parses the whole program before execution, resets the execution counter,
and executes the ProgramNode in the global environment. Consequently, a syntax
error anywhere prevents execution from beginning. Runtime errors can occur after
earlier statements have already executed.

## 2. How values are stored and retrieved

Each Environment has `values`, a dictionary mapping names to values, and an
optional `parent` pointing at its enclosing scope. There is no global flat table
for all blocks. `define()` inserts into the current dictionary, `resolve()` walks
outward until a name is found, `get()` retrieves it, and `assign()` updates that
resolved dictionary. Unsuccessful lookup raises EmeraldRuntimeError.

Core code from environment.py:

```python
def resolve(self, name, node=None):
    scope = self
    while scope is not None:
        if name in scope.values:
            return scope
        scope = scope.parent
    raise EmeraldRuntimeError(f"undefined variable '{name}'", node)
```

For `let x=10; let y=x+5;`, the first declaration stores `x: 10`. Evaluating the
second declaration looks up x, adds 5, and stores `y: 15`. For
`{ let x=20; print(x); } print(x);`, the inner dictionary holds a separate x;
the output is 20 then 10. With `{ x=20; }`, assignment instead finds and updates
the outer x. Lookup cost is proportional to nesting depth; dictionary operations
are average constant time within each scope.

## 3. Statements versus expressions

`execute(node, env)` handles effects. A declaration evaluates its initializer
before storing the result. Assignment locates its target before evaluating the
right side. A print statement evaluates a value and writes its formatted text.
An if statement evaluates only its selected branch. A while statement reevaluates
its condition before every iteration. Block statements allocate a child environment.

`evaluate(node, env)` returns a value. Number/boolean nodes return their values,
variable nodes use `env.get`, array nodes evaluate their elements in order, and
binary nodes evaluate operands and apply the requested operation. Function
arguments and ordinary binary operands are evaluated left to right.

## 4. Precedence and arithmetic

The parser already represents `2+3*4` as `+(2, *(3, 4))`. Recursive evaluation
first computes 3*4, then adds 2, producing 14. `(2+3)*4` has a different tree and
produces 20. The interpreter neither reparses source nor reimplements precedence.

`number()` accepts only exact Python int/float types, excluding bool. Division
checks the divisor before calculation. Overflow and non-finite float results
are errors. Comparisons produce booleans. Equality accepts numeric pairs or
boolean pairs, so `2 == 2.0` is true and `true == 1` is a runtime error.

## 5. Control flow

Conditions pass through `boolean()`, avoiding implicit Python truthiness.
For `while(x<=5)`, the condition sees the current x each time; the body assignment
updates the enclosing x. `and` and `or` inspect their left operand first and skip
the right operand when the result is already known. Therefore
`false and (1/0 == 0)` safely evaluates to false.

A for loop allocates a loop environment, executes initialization once, repeatedly
checks the condition, executes the body, then executes the update. The loop's
declared counter does not escape. AST visits count toward a configurable budget;
exceeding the budget raises a runtime error rather than hanging indefinitely.

## 6. Functions and arrays

A Function stores its declaration and defining Environment, called its closure.
A call verifies arity, evaluates arguments, creates a child of that closure, and
binds parameters. It never uses the caller's local scope as the parent. This is
lexical scoping. Recursive calls can find the function in its defining scope.

ReturnSignal is an internal exception carrying a return value through nested
blocks and loops. The nearest function call catches it; `finally` restores the
call-depth counter even if an error occurs. A return outside a function is an
explicit runtime error. Excessive recursion is converted to a language error.

Arrays are Python lists used only through the interpreter's explicit rules.
`array_slot()` checks that the value is an array and the index is an integer in
range. Indexed assignment mutates the list. Arrays have reference semantics;
`let b=a` creates an alias. Printing detects cycles to prevent recursive output
from crashing when an array contains itself.

## 7. Error boundaries

Environment and interpreter errors use EmeraldRuntimeError, carrying source
line/column from the AST. LexerError and ParseError remain separate categories.
The CLI catches known language and file errors, prints a readable message to
stderr, and exits 1. Usage errors exit 2. It does not catch every Exception,
which would hide programming defects. The execution budget is a classroom
guardrail, not a security sandbox or a complete memory/time limit.

## 8. Verification strategy

The fixed expected files were specified from the intended semantics before
running the interpreter. `verify_examples.py` captures actual CLI results and
checks exact text, exit status, and the absence of output on the wrong stream.
The unit suite checks positive behavior and invalid inputs, including scope,
short-circuit behavior, function closures, recursion, bounds, and error locations.
The original lexer and parser suites are also run separately as regression checks.

## 9. How to explain the implementation in a demonstration

Run program 01 and show x/y in Environment.values. Run program 02 and show its
AST with `python emerald_parser.py programs/02_arithmetic.em --diagram`. Run
program 04 for both branches and program 05 for repeated condition evaluation.
Use program 06 to explain inner dictionaries and outward assignment. Finally,
run each error program and explain why it exits with status 1.
