# Part 5 Architecture

## Execution pipeline
    Emerald .em source
            |
            v
    Lexer: characters -> tokens (including break/continue)
            |
            v
    Parser: tokens -> AST
            |
            v
    Interpreter.execute / evaluate
       |             |                  |
       v             v                  v
    Environment    Function calls     Loop controls
    dictionaries   + ReturnSignal     + BreakSignal / ContinueSignal
       |             |                  |
       +-------------+------------------+
                     |
                     v
                output / located error

## Scope example
    Global Environment: {x: 10, test: Function}
          ^
          | parent = defining environment
    Call Environment: {x: 20}

The call prints its local x (20). After returning, global print resolves x to 10.
Environment.resolve walks outward; define writes only to the current scope;
assign changes the closest existing binding. This supports shadowing and global
assignment without making local variables global.

## Function call
    lookup function -> check argument count -> evaluate arguments left to right
       -> create Environment(function.closure) -> bind parameters
       -> execute function body -> catch ReturnSignal -> return value

FunctionNode stores name, parameters, and body. CallNode stores name and arguments.
ReturnNode stores its optional expression. No explicit return produces nil.
The function body's declarations share the parameter scope. Nested blocks create
children. Functions retain their defining environment, supporting closures and
recursion. No host eval or exec is used.

## Extension
BreakNode and ContinueNode retain line and column, like all other AST nodes.
Loops catch the signals from their own body. Break skips the update and exits;
continue in a for loop still reaches its update. Nested loops catch the nearest
signal. ReturnSignal passes through loops until the function catches it.
Loop depth is reset for each call, so functions cannot control caller loops.
Finally blocks restore loop and call state after returns and runtime errors.

## Assignment mapping
Functions: interpreter.py Function and CallNode/FunctionNode/ReturnNode handling.
Scope: environment.py plus call_env and function.closure in interpreter.py.
Extension: new tokens, nodes, parser loop_control, signals and loop execution.
Tests: programs 09–17, test_extension.py, inherited test_interpreter.py.
Grammar: full GRAMMAR.md with break/continue productions and execution rules.
