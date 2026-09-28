"""Tree-walking Emerald interpreter. No Python eval or exec is used."""
import argparse
from dataclasses import dataclass
import math
import sys

import ast_nodes as ast
from emerald_parser import parse_source, ParseError
from lexer import LexerError
from environment import Environment, EmeraldRuntimeError


@dataclass
class Function:
    declaration: ast.FunctionNode
    closure: Environment


class ReturnSignal(Exception):
    """Internal control flow; never exposed as a language error."""
    def __init__(self, value):
        self.value = value


def format_value(value, seen=None):
    if value is None:
        return "nil"
    if type(value) is bool:
        return "true" if value else "false"
    if isinstance(value, Function):
        return f"<function {value.declaration.name}>"
    if isinstance(value, list):
        seen = set() if seen is None else seen
        if id(value) in seen:
            return "[...]"
        seen.add(id(value))
        result = "[" + ", ".join(format_value(v, seen) for v in value) + "]"
        seen.remove(id(value))
        return result
    return str(value)


class Interpreter:
    def __init__(self, output=None, max_steps=100000):
        if max_steps < 1:
            raise ValueError("max_steps must be positive")
        self.globals = Environment()
        self.output = sys.stdout if output is None else output
        self.max_steps = max_steps
        self.steps = 0
        self.call_depth = 0

    def fail(self, message, node):
        raise EmeraldRuntimeError(message, node)

    def tick(self, node):
        self.steps += 1
        if self.steps > self.max_steps:
            self.fail(f"execution limit of {self.max_steps} AST visits exceeded", node)

    def number(self, value, node):
        # bool is a subclass of int in Python, but is not a number in Emerald.
        if type(value) not in (int, float):
            self.fail("numeric operand required", node)
        if type(value) is float and not math.isfinite(value):
            self.fail("non-finite numeric value", node)
        return value

    def boolean(self, value, node):
        if type(value) is not bool:
            self.fail("boolean value required", node)
        return value

    def run(self, source):
        program = parse_source(source)
        self.steps = 0
        try:
            self.execute(program, self.globals)
        except RecursionError:
            self.fail("recursion limit exceeded", program)
        return self.globals

    def execute_block(self, block, env):
        for statement in block.statements:
            self.execute(statement, env)

    def execute(self, node, env):
        self.tick(node)
        if isinstance(node, ast.ProgramNode):
            self.execute_block(node, env)
        elif isinstance(node, ast.BlockNode):
            self.execute_block(node, Environment(env))
        elif isinstance(node, ast.DeclarationNode):
            env.define(node.name, self.evaluate(node.value, env), node)
        elif isinstance(node, ast.AssignmentNode):
            if isinstance(node.target, ast.VariableNode):
                scope = env.resolve(node.target.name, node.target)
                scope.assign(node.target.name, self.evaluate(node.value, env), node)
            else:
                array, index = self.array_slot(node.target, env)
                array[index] = self.evaluate(node.value, env)
        elif isinstance(node, ast.PrintNode):
            print(format_value(self.evaluate(node.value, env)), file=self.output)
        elif isinstance(node, ast.ExpressionStatementNode):
            self.evaluate(node.expression, env)
        elif isinstance(node, ast.IfNode):
            condition = self.boolean(self.evaluate(node.condition, env), node.condition)
            branch = node.then_branch if condition else node.else_branch
            if branch is not None:
                self.execute(branch, env)
        elif isinstance(node, ast.WhileNode):
            while self.boolean(self.evaluate(node.condition, env), node.condition):
                self.execute(node.body, env)
        elif isinstance(node, ast.ForNode):
            loop_env = Environment(env)
            self.execute(node.init, loop_env)
            while self.boolean(self.evaluate(node.condition, loop_env), node.condition):
                self.execute(node.body, loop_env)
                self.execute(node.update, loop_env)
        elif isinstance(node, ast.FunctionNode):
            if len(set(node.parameters)) != len(node.parameters):
                self.fail("duplicate function parameter", node)
            env.define(node.name, Function(node, env), node)
        elif isinstance(node, ast.ReturnNode):
            if self.call_depth == 0:
                self.fail("return outside a function", node)
            raise ReturnSignal(None if node.value is None else self.evaluate(node.value, env))
        else:
            self.fail(f"unsupported statement {type(node).__name__}", node)

    def array_slot(self, node, env):
        array = env.get(node.name, node)
        if type(array) is not list:
            self.fail(f"'{node.name}' is not an array", node)
        index = self.evaluate(node.index, env)
        if type(index) is not int:
            self.fail("array index must be an integer", node)
        if not 0 <= index < len(array):
            self.fail(f"array index {index} out of bounds for length {len(array)}", node)
        return array, index

    def evaluate(self, node, env):
        self.tick(node)
        if isinstance(node, ast.NumberNode):
            return self.number(node.value, node)
        if isinstance(node, ast.BooleanNode):
            return node.value
        if isinstance(node, ast.VariableNode):
            return env.get(node.name, node)
        if isinstance(node, ast.ArrayNode):
            return [self.evaluate(item, env) for item in node.elements]
        if isinstance(node, ast.IndexNode):
            array, index = self.array_slot(node, env)
            return array[index]
        if isinstance(node, ast.UnaryOpNode):
            value = self.evaluate(node.operand, env)
            if node.operator == "-":
                return -self.number(value, node)
            return not self.boolean(value, node)
        if isinstance(node, ast.BinaryOpNode):
            return self.binary(node, env)
        if isinstance(node, ast.CallNode):
            function = env.get(node.name, node)
            if not isinstance(function, Function):
                self.fail(f"'{node.name}' is not callable", node)
            declaration = function.declaration
            if len(node.arguments) != len(declaration.parameters):
                self.fail(f"'{node.name}' expects {len(declaration.parameters)} arguments, got {len(node.arguments)}", node)
            arguments = [self.evaluate(arg, env) for arg in node.arguments]
            call_env = Environment(function.closure)
            for name, value in zip(declaration.parameters, arguments):
                call_env.define(name, value, node)
            self.call_depth += 1
            try:
                self.execute_block(declaration.body, call_env)
            except ReturnSignal as result:
                return result.value
            finally:
                self.call_depth -= 1
            return None
        self.fail(f"unsupported expression {type(node).__name__}", node)

    def binary(self, node, env):
        op = node.operator
        left = self.evaluate(node.left, env)
        if op in ("and", "or"):
            left = self.boolean(left, node)
            if (op == "and" and not left) or (op == "or" and left):
                return left
            return self.boolean(self.evaluate(node.right, env), node)
        right = self.evaluate(node.right, env)
        if op in ("==", "!="):
            numeric = type(left) in (int, float) and type(right) in (int, float)
            if not numeric and not (type(left) is bool and type(right) is bool):
                self.fail("equality requires two numbers or two booleans", node)
            equal = left == right
            return equal if op == "==" else not equal
        left, right = self.number(left, node), self.number(right, node)
        if op == "/" and right == 0:
            self.fail("division by zero", node)
        operations = {
            "+": lambda: left + right, "-": lambda: left - right,
            "*": lambda: left * right, "/": lambda: left / right,
            "<": lambda: left < right, ">": lambda: left > right,
            "<=": lambda: left <= right, ">=": lambda: left >= right,
        }
        if op not in operations:
            self.fail(f"unsupported operator '{op}'", node)
        try:
            result = operations[op]()
        except OverflowError:
            self.fail("numeric overflow", node)
        return self.number(result, node) if type(result) is not bool else result


def main(argv=None):
    cli = argparse.ArgumentParser(description="Execute an Emerald source file")
    cli.add_argument("source")
    cli.add_argument("--max-steps", type=int, default=100000,
                     help="maximum AST visits (default: 100000)")
    args = cli.parse_args(argv)
    if args.max_steps < 1:
        cli.error("--max-steps must be positive")
    try:
        with open(args.source, encoding="utf-8") as source:
            Interpreter(max_steps=args.max_steps).run(source.read())
    except (EmeraldRuntimeError, LexerError, ParseError, OSError, UnicodeError) as error:
        print(error, file=sys.stderr)
        return 1
    except RecursionError:
        print("Runtime error: source nesting exceeds recursion limit", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
