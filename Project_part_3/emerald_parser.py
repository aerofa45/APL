"""Recursive-descent parser for Emerald.

Each grammar rule from the Part 1 BNF (see GRAMMAR.md) is one method. The
parser consumes the token list produced by the Part 2 lexer and returns an
AST rooted at a ProgramNode. It stops at the first syntax error.
"""
import ast_nodes as ast
from lexer import Lexer, LexerError
from token_definitions import TokenType as T


class ParseError(Exception):
    pass


COMPARISON_OPERATORS = (T.LESS, T.GREATER, T.LESS_EQUAL, T.GREATER_EQUAL)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0


    def peek(self, offset=0):
        index = min(self.pos + offset, len(self.tokens) - 1)
        return self.tokens[index]

    def check(self, *types):
        return self.peek().token_type in types

    def advance(self):
        token = self.peek()
        if token.token_type != T.EOF:
            self.pos += 1
        return token

    def match(self, *types):
        if self.check(*types):
            return self.advance()
        return None

    def error(self, message, token=None):
        token = token or self.peek()
        found = "end of input" if token.token_type == T.EOF else repr(token.lexeme)
        return ParseError(
            f"Syntax error at line {token.line}, column {token.column}: "
            f"{message}, found {found}"
        )

    def expect(self, token_type, description):
        if self.check(token_type):
            return self.advance()
        raise self.error(f"expected {description}")

    def expect_identifier(self, context):
        return self.expect(T.IDENTIFIER, f"identifier {context}")


    def parse(self):
        first = self.peek()
        statements = []
        while not self.check(T.EOF):
            statements.append(self.statement())
        return ast.ProgramNode(statements, line=first.line, column=first.column)

    def statement(self):
        handlers = {
            T.LET: self.declaration,
            T.PRINT: self.print_statement,
            T.IF: self.if_statement,
            T.WHILE: self.while_statement,
            T.FOR: self.for_statement,
            T.FUNC: self.function_definition,
            T.RETURN: self.return_statement,
            T.LEFT_BRACE: self.block,
        }
        handler = handlers.get(self.peek().token_type)
        if handler:
            return handler()
        return self.assignment_or_expression_statement()

    def block(self):
        start = self.expect(T.LEFT_BRACE, "'{'")
        statements = []
        while not self.check(T.RIGHT_BRACE, T.EOF):
            statements.append(self.statement())
        self.expect(T.RIGHT_BRACE, "'}' to close block")
        return ast.BlockNode(statements, line=start.line, column=start.column)

    def declaration(self):
        start = self.advance()  # let
        name = self.expect_identifier("after 'let'")
        self.expect(T.ASSIGN, "'=' (variables must be initialized)")
        value = self.expression()
        self.expect(T.SEMICOLON, "';' after declaration")
        return ast.DeclarationNode(name.lexeme, value, line=start.line, column=start.column)

    def print_statement(self):
        start = self.advance()  # print
        self.expect(T.LEFT_PAREN, "'(' after 'print'")
        value = self.expression()
        self.expect(T.RIGHT_PAREN, "')' after print argument")
        self.expect(T.SEMICOLON, "';' after print statement")
        return ast.PrintNode(value, line=start.line, column=start.column)

    def if_statement(self):
        start = self.advance()  # if
        self.expect(T.LEFT_PAREN, "'(' after 'if'")
        condition = self.expression()
        self.expect(T.RIGHT_PAREN, "')' after condition")
        then_branch = self.block()
        else_branch = None
        if self.match(T.ELSE):
            else_branch = self.block()
        return ast.IfNode(condition, then_branch, else_branch,
                          line=start.line, column=start.column)

    def while_statement(self):
        start = self.advance()  # while
        self.expect(T.LEFT_PAREN, "'(' after 'while'")
        condition = self.expression()
        self.expect(T.RIGHT_PAREN, "')' after condition")
        body = self.block()
        return ast.WhileNode(condition, body, line=start.line, column=start.column)

    def for_statement(self):
        start = self.advance()  # for
        self.expect(T.LEFT_PAREN, "'(' after 'for'")
        init = self.for_init()
        self.expect(T.SEMICOLON, "';' after for-loop initializer")
        condition = self.expression()
        self.expect(T.SEMICOLON, "';' after for-loop condition")
        update = self.for_update()
        self.expect(T.RIGHT_PAREN, "')' after for-loop header")
        body = self.block()
        return ast.ForNode(init, condition, update, body,
                           line=start.line, column=start.column)

    def for_init(self):
        if self.check(T.LET):
            start = self.advance()
            name = self.expect_identifier("after 'let'")
            self.expect(T.ASSIGN, "'=' in for-loop initializer")
            value = self.expression()
            return ast.DeclarationNode(name.lexeme, value,
                                       line=start.line, column=start.column)
        if self.check(T.IDENTIFIER):
            name = self.advance()
            self.expect(T.ASSIGN, "'=' in for-loop initializer")
            value = self.expression()
            target = ast.VariableNode(name.lexeme, line=name.line, column=name.column)
            return ast.AssignmentNode(target, value, line=name.line, column=name.column)
        raise self.error("expected 'let' or identifier in for-loop initializer")

    def for_update(self):
        name = self.expect_identifier("in for-loop update")
        target = self.assignment_target(name)
        self.expect(T.ASSIGN, "'=' in for-loop update")
        value = self.expression()
        return ast.AssignmentNode(target, value, line=name.line, column=name.column)

    def function_definition(self):
        start = self.advance()  # func
        name = self.expect_identifier("after 'func'")
        self.expect(T.LEFT_PAREN, "'(' after function name")
        parameters = []
        if not self.check(T.RIGHT_PAREN):
            parameters.append(self.expect_identifier("as parameter").lexeme)
            while self.match(T.COMMA):
                parameters.append(self.expect_identifier("as parameter").lexeme)
        self.expect(T.RIGHT_PAREN, "')' after parameters")
        body = self.block()
        return ast.FunctionNode(name.lexeme, parameters, body,
                                line=start.line, column=start.column)

    def return_statement(self):
        start = self.advance()  # return
        value = None
        if not self.check(T.SEMICOLON):
            value = self.expression()
        self.expect(T.SEMICOLON, "';' after return")
        return ast.ReturnNode(value, line=start.line, column=start.column)

    def assignment_target(self, name):
        """Build the target after an identifier: `name` or `name[expr]`."""
        if self.match(T.LEFT_BRACKET):
            index = self.expression()
            self.expect(T.RIGHT_BRACKET, "']' after index")
            return ast.IndexNode(name.lexeme, index, line=name.line, column=name.column)
        return ast.VariableNode(name.lexeme, line=name.line, column=name.column)

    def assignment_or_expression_statement(self):
        start = self.peek()
        expr = self.expression()
        if self.check(T.ASSIGN):
            equals = self.advance()
            # A target must be written as `name` or `name[expr]`, so `(x) = 1` is rejected.
            valid = (start.token_type == T.IDENTIFIER
                     and isinstance(expr, (ast.VariableNode, ast.IndexNode)))
            if not valid:
                raise ParseError(
                    f"Syntax error at line {start.line}, column {start.column}: "
                    f"invalid assignment target (expected identifier or array element "
                    f"before '=' at column {equals.column})"
                )
            value = self.expression()
            self.expect(T.SEMICOLON, "';' after assignment")
            return ast.AssignmentNode(expr, value, line=start.line, column=start.column)
        self.expect(T.SEMICOLON, "';' after expression")
        return ast.ExpressionStatementNode(expr, line=start.line, column=start.column)

    # ----- expressions (lowest to highest precedence) -------------------

    def expression(self):
        return self.logical_or()

    def binary_level(self, next_level, *operators):
        left = next_level()
        while self.check(*operators):
            op = self.advance()
            right = next_level()
            left = ast.BinaryOpNode(op.lexeme, left, right, line=op.line, column=op.column)
        return left

    def logical_or(self):
        return self.binary_level(self.logical_and, T.OR)

    def logical_and(self):
        return self.binary_level(self.equality, T.AND)

    def equality(self):
        return self.binary_level(self.comparison, T.EQUAL_EQUAL, T.NOT_EQUAL)

    def comparison(self):
        return self.binary_level(self.arith_expr, *COMPARISON_OPERATORS)

    def arith_expr(self):
        return self.binary_level(self.term, T.PLUS, T.MINUS)

    def term(self):
        return self.binary_level(self.factor, T.MULTIPLY, T.DIVIDE)

    def factor(self):
        token = self.peek()
        kind = token.token_type

        if kind in (T.MINUS, T.NOT):
            self.advance()
            operand = self.factor()
            return ast.UnaryOpNode(token.lexeme, operand, line=token.line, column=token.column)

        if kind == T.INTEGER:
            self.advance()
            return ast.NumberNode(int(token.lexeme), line=token.line, column=token.column)
        if kind == T.DECIMAL:
            self.advance()
            return ast.NumberNode(float(token.lexeme), line=token.line, column=token.column)
        if kind in (T.TRUE, T.FALSE):
            self.advance()
            return ast.BooleanNode(kind == T.TRUE, line=token.line, column=token.column)

        if kind == T.IDENTIFIER:
            self.advance()
            if self.match(T.LEFT_PAREN):
                arguments = self.argument_list()
                self.expect(T.RIGHT_PAREN, "')' after arguments")
                return ast.CallNode(token.lexeme, arguments, line=token.line, column=token.column)
            if self.match(T.LEFT_BRACKET):
                index = self.expression()
                self.expect(T.RIGHT_BRACKET, "']' after index")
                return ast.IndexNode(token.lexeme, index, line=token.line, column=token.column)
            return ast.VariableNode(token.lexeme, line=token.line, column=token.column)

        if kind == T.LEFT_PAREN:
            self.advance()
            inner = self.expression()
            self.expect(T.RIGHT_PAREN, "')' to close grouping")
            return inner

        if kind == T.LEFT_BRACKET:
            self.advance()
            elements = []
            if not self.check(T.RIGHT_BRACKET):
                elements.append(self.expression())
                while self.match(T.COMMA):
                    elements.append(self.expression())
            self.expect(T.RIGHT_BRACKET, "']' to close array literal")
            return ast.ArrayNode(elements, line=token.line, column=token.column)

        raise self.error("expected expression")

    def argument_list(self):
        arguments = []
        if not self.check(T.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(T.COMMA):
                arguments.append(self.expression())
        return arguments


def parse_source(source):
    """Lex and parse Emerald source text; return a ProgramNode."""
    return Parser(Lexer(source).tokenize()).parse()


def parse_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return parse_source(file.read())


if __name__ == "__main__":
    import sys

    from ast_diagram import format_program_diagram

    arguments = [a for a in sys.argv[1:] if a != "--diagram"]
    diagram = len(arguments) != len(sys.argv) - 1
    if len(arguments) != 1:
        print("Usage: python emerald_parser.py <source-file> [--diagram]")
        sys.exit(1)

    try:
        program = parse_file(arguments[0])
        print(format_program_diagram(program) if diagram else ast.format_tree(program))
    except FileNotFoundError:
        print(f"Error: file {arguments[0]!r} was not found.")
        sys.exit(1)
    except (LexerError, ParseError) as error:
        print(error)
        sys.exit(1)
    except (OSError, UnicodeError) as error:
        print(f"Error: {error}")
        sys.exit(1)
