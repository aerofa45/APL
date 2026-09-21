import subprocess
import sys
import unittest
from pathlib import Path

from ast_nodes import (
    ArrayNode, AssignmentNode, BinaryOpNode, BlockNode, BooleanNode, CallNode,
    DeclarationNode, ExpressionStatementNode, ForNode, FunctionNode, IfNode,
    IndexNode, NumberNode, PrintNode, ProgramNode, ReturnNode, UnaryOpNode,
    VariableNode, WhileNode, format_tree,
)
from ast_diagram import draw, format_program_diagram
from emerald_parser import ParseError, parse_source
from lexer import LexerError

ROOT = Path(__file__).resolve().parent


def expr(source):
    """Parse `let v = <source>;` and return the initializer expression."""
    return parse_source(f"let v = {source};").statements[0].value


def var(name="x"):
    return VariableNode(name)


def num(value):
    return NumberNode(value)


class TestAssignmentRequirements(unittest.TestCase):
    """The behaviors required by the Part 3 task description."""

    def test_precedence_2_plus_3_times_4(self):
        tree = parse_source("print(2 + 3 * 4);")
        self.assertEqual(tree, ProgramNode([PrintNode(
            BinaryOpNode("+", num(2), BinaryOpNode("*", num(3), num(4))))]))

    def test_parentheses_override_precedence(self):
        self.assertEqual(expr("(2 + 3) * 4"),
                         BinaryOpNode("*", BinaryOpNode("+", num(2), num(3)), num(4)))

    def test_numbers_and_variables(self):
        self.assertEqual(expr("7"), num(7))
        self.assertEqual(expr("total"), var("total"))

    def test_assignment(self):
        self.assertEqual(parse_source("x = x + 1;").statements[0],
                         AssignmentNode(var(), BinaryOpNode("+", var(), num(1))))
        self.assertEqual(parse_source("let x = 10;").statements[0],
                         DeclarationNode("x", num(10)))

    def test_print_statement(self):
        self.assertEqual(parse_source("print(x);").statements[0], PrintNode(var()))

    def test_multiple_statements(self):
        tree = parse_source("let x = 1;\nlet y = 2;\nprint(x + y);")
        self.assertEqual(len(tree.statements), 3)
        self.assertEqual([type(s) for s in tree.statements],
                         [DeclarationNode, DeclarationNode, PrintNode])

    def test_let_x_equals_semicolon_is_invalid(self):
        with self.assertRaises(ParseError) as caught:
            parse_source("let x = ;")
        self.assertIn("line 1, column 9", str(caught.exception))
        self.assertIn("expected expression", str(caught.exception))


class TestStatements(unittest.TestCase):
    def test_empty_program(self):
        self.assertEqual(parse_source(""), ProgramNode([]))
        self.assertEqual(parse_source("// only a comment\n"), ProgramNode([]))

    def test_integer_and_decimal_literals(self):
        self.assertEqual(expr("3"), num(3))
        self.assertIsInstance(expr("3").value, int)
        self.assertEqual(expr("3.5"), num(3.5))
        self.assertIsInstance(expr("3.5").value, float)

    def test_if_without_else(self):
        stmt = parse_source("if (x < y) { print(x); }").statements[0]
        self.assertEqual(stmt, IfNode(BinaryOpNode("<", var(), var("y")),
                                      BlockNode([PrintNode(var())]), None))

    def test_if_else(self):
        stmt = parse_source("if (a) { print(a); } else { print(b); }").statements[0]
        self.assertEqual(stmt.else_branch, BlockNode([PrintNode(var("b"))]))

    def test_while(self):
        stmt = parse_source("while (x < 10) { x = x + 1; }").statements[0]
        self.assertEqual(stmt, WhileNode(
            BinaryOpNode("<", var(), num(10)),
            BlockNode([AssignmentNode(var(), BinaryOpNode("+", var(), num(1)))])))

    def test_for_with_let_initializer(self):
        stmt = parse_source(
            "for (let i = 0; i < 5; i = i + 1) { print(i); }").statements[0]
        self.assertEqual(stmt, ForNode(
            DeclarationNode("i", num(0)),
            BinaryOpNode("<", var("i"), num(5)),
            AssignmentNode(var("i"), BinaryOpNode("+", var("i"), num(1))),
            BlockNode([PrintNode(var("i"))])))

    def test_for_with_assignment_initializer_and_indexed_update(self):
        stmt = parse_source("for (i = 0; i < 3; a[i] = 1) { }").statements[0]
        self.assertEqual(stmt.init, AssignmentNode(var("i"), num(0)))
        self.assertEqual(stmt.update, AssignmentNode(IndexNode("a", var("i")), num(1)))
        self.assertEqual(stmt.body, BlockNode([]))

    def test_function_definition(self):
        stmt = parse_source(
            "func add(a, b) { let r = a + b; return r; }").statements[0]
        self.assertEqual(stmt, FunctionNode("add", ["a", "b"], BlockNode([
            DeclarationNode("r", BinaryOpNode("+", var("a"), var("b"))),
            ReturnNode(var("r")),
        ])))

    def test_function_without_parameters(self):
        stmt = parse_source("func f() { return; }").statements[0]
        self.assertEqual(stmt, FunctionNode("f", [], BlockNode([ReturnNode(None)])))

    def test_expression_statement(self):
        self.assertEqual(parse_source("f(1);").statements[0],
                         ExpressionStatementNode(CallNode("f", [num(1)])))

    def test_standalone_block(self):
        self.assertEqual(parse_source("{ let a = 1; }").statements[0],
                         BlockNode([DeclarationNode("a", num(1))]))

    def test_nested_function_definition_is_a_statement(self):
        stmt = parse_source("func f() { func g() { } }").statements[0]
        self.assertIsInstance(stmt.body.statements[0], FunctionNode)


class TestExpressions(unittest.TestCase):
    def test_left_associativity(self):
        self.assertEqual(expr("10 - 4 - 3"),
                         BinaryOpNode("-", BinaryOpNode("-", num(10), num(4)), num(3)))
        self.assertEqual(expr("8 / 4 / 2"),
                         BinaryOpNode("/", BinaryOpNode("/", num(8), num(4)), num(2)))

    def test_full_precedence_chain(self):
        # or < and < equality < comparison < additive < multiplicative
        self.assertEqual(
            expr("a or b and c == d < e + f * g"),
            BinaryOpNode("or", var("a"), BinaryOpNode("and", var("b"), BinaryOpNode(
                "==", var("c"), BinaryOpNode("<", var("d"), BinaryOpNode(
                    "+", var("e"), BinaryOpNode("*", var("f"), var("g"))))))))

    def test_all_comparison_operators(self):
        for op in ("==", "!=", "<", ">", "<=", ">="):
            self.assertEqual(expr(f"a {op} b"), BinaryOpNode(op, var("a"), var("b")))

    def test_unary_binds_tighter_than_binary(self):
        self.assertEqual(expr("-a * b"),
                         BinaryOpNode("*", UnaryOpNode("-", var("a")), var("b")))
        self.assertEqual(expr("not a and b"),
                         BinaryOpNode("and", UnaryOpNode("not", var("a")), var("b")))

    def test_repeated_unary(self):
        self.assertEqual(expr("- -a"), UnaryOpNode("-", UnaryOpNode("-", var("a"))))
        self.assertEqual(expr("not not a"),
                         UnaryOpNode("not", UnaryOpNode("not", var("a"))))

    def test_booleans(self):
        self.assertEqual(expr("true"), BooleanNode(True))
        self.assertEqual(expr("false"), BooleanNode(False))

    def test_call_arguments(self):
        self.assertEqual(expr("f()"), CallNode("f", []))
        self.assertEqual(expr("f(1, g(2), a + b)"),
                         CallNode("f", [num(1), CallNode("g", [num(2)]),
                                        BinaryOpNode("+", var("a"), var("b"))]))

    def test_array_literal(self):
        self.assertEqual(expr("[]"), ArrayNode([]))
        self.assertEqual(expr("[1, 2 + 3]"),
                         ArrayNode([num(1), BinaryOpNode("+", num(2), num(3))]))

    def test_index_access(self):
        self.assertEqual(expr("a[i + 1]"),
                         IndexNode("a", BinaryOpNode("+", var("i"), num(1))))
        self.assertEqual(expr("a[b[0]]"), IndexNode("a", IndexNode("b", num(0))))

    def test_index_assignment(self):
        self.assertEqual(parse_source("scores[1] = 100;").statements[0],
                         AssignmentNode(IndexNode("scores", num(1)), num(100)))

    def test_positions_are_recorded(self):
        stmt = parse_source("\n  let x = 1 + 2;").statements[0]
        self.assertEqual((stmt.line, stmt.column), (2, 3))
        self.assertEqual((stmt.value.line, stmt.value.column), (2, 13))  # the '+'


class TestSyntaxErrors(unittest.TestCase):
    def assertParseError(self, source, *fragments):
        with self.assertRaises(ParseError) as caught:
            parse_source(source)
        message = str(caught.exception)
        for fragment in fragments:
            self.assertIn(fragment, message)

    def test_missing_semicolon_after_declaration(self):
        self.assertParseError("let x = 1\nprint(x);",
                              "line 2, column 1", "expected ';'", "'print'")

    def test_declaration_requires_initializer(self):
        self.assertParseError("let x;", "line 1, column 6", "expected '='")

    def test_declaration_requires_identifier(self):
        self.assertParseError("let 5 = 1;", "identifier after 'let'")

    def test_keyword_cannot_be_identifier(self):
        self.assertParseError("let print = 1;", "identifier after 'let'")

    def test_missing_expression(self):
        self.assertParseError("let x = ;", "line 1, column 9", "expected expression")
        self.assertParseError("let x = 1 + ;", "expected expression")

    def test_unbalanced_parenthesis(self):
        self.assertParseError("let x = (1 + 2;", "expected ')'")
        self.assertParseError("let x = 1 + 2);", "expected ';'", "')'")

    def test_unclosed_block_reports_end_of_input(self):
        self.assertParseError("if (a) {\n print(a);\n", "expected '}'",
                              "end of input")

    def test_stray_closing_brace(self):
        self.assertParseError("}", "expected expression", "'}'")

    def test_if_requires_parentheses_and_block(self):
        self.assertParseError("if a { }", "expected '(' after 'if'")
        self.assertParseError("if (a) print(a);", "expected '{'")

    def test_else_if_is_not_in_the_grammar(self):
        self.assertParseError("if (a) { } else if (b) { }", "expected '{'")

    def test_for_header_errors(self):
        self.assertParseError("for (i < 3; i < 5; i = i + 1) { }", "expected '='")
        self.assertParseError("for (let i = 0, i < 5; i = i + 1) { }",
                              "expected ';' after for-loop initializer")
        self.assertParseError("for (let i = 0; i < 5; i + 1) { }", "expected '='")
        self.assertParseError("for (let i = 0; i < 5; i = i + 1;) { }",
                              "expected ')' after for-loop header")

    def test_function_definition_errors(self):
        self.assertParseError("func (a) { }", "identifier after 'func'")
        self.assertParseError("func f(a,) { }", "identifier as parameter")
        self.assertParseError("func f(1) { }", "identifier as parameter")
        self.assertParseError("func f(a) return a;", "expected '{'")

    def test_call_argument_errors(self):
        self.assertParseError("f(1,);", "expected expression")
        self.assertParseError("f(1 2);", "expected ')' after arguments")

    def test_invalid_assignment_targets(self):
        self.assertParseError("x + y = 3;", "line 1, column 1", "invalid assignment target")
        self.assertParseError("5 = 3;", "invalid assignment target")
        self.assertParseError("(x) = 3;", "invalid assignment target")
        self.assertParseError("f(1) = 3;", "invalid assignment target")

    def test_array_errors(self):
        self.assertParseError("let a = [1, 2;", "expected ']'")
        self.assertParseError("let a = [1,];", "expected expression")
        self.assertParseError("a[0;", "expected ']' after index")

    def test_chained_indexing_is_not_in_the_grammar(self):
        self.assertParseError("let v = a[0][1];", "expected ';'")

    def test_print_requires_parentheses(self):
        self.assertParseError("print x;", "expected '(' after 'print'")
        self.assertParseError("print(x;", "expected ')' after print argument")

    def test_lexical_errors_propagate(self):
        with self.assertRaises(LexerError):
            parse_source("let x = 1 @ 2;")


class TestExamplePrograms(unittest.TestCase):
    def run_cli(self, name):
        return subprocess.run(
            [sys.executable, str(ROOT / "emerald_parser.py"),
             str(ROOT / "test_inputs" / name)],
            capture_output=True, text=True)

    def test_valid_examples_parse(self):
        for path in sorted((ROOT / "test_inputs").glob("test*.em")):
            if "invalid" in path.name:
                continue
            with self.subTest(path.name):
                result = self.run_cli(path.name)
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertTrue(result.stdout.startswith("ProgramNode"))

    def test_invalid_examples_fail_with_status_1(self):
        for path in sorted((ROOT / "test_inputs").glob("test*invalid*.em")):
            with self.subTest(path.name):
                result = self.run_cli(path.name)
                self.assertEqual(result.returncode, 1)
                self.assertIn("Syntax error at line", result.stdout)

    def test_missing_file_and_usage(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "emerald_parser.py"), "nope.em"],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("was not found", result.stdout)
        result = subprocess.run(
            [sys.executable, str(ROOT / "emerald_parser.py")],
            capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Usage", result.stdout)


class TestDiagram(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "emerald_parser.py"), *args],
                              capture_output=True, text=True)

    def test_diagram_for_2_plus_3_times_4(self):
        self.assertEqual(draw(expr("2 + 3 * 4")), "\n".join([
            "  +",
            " / \\",
            "/   \\",
            "2   *",
            "   / \\",
            "   3 4",
        ]))

    def test_diagram_shows_multiplication_below_addition(self):
        lines = draw(expr("2 + 3 * 4")).split("\n")
        plus = next(i for i, l in enumerate(lines) if "+" in l)
        star = next(i for i, l in enumerate(lines) if "*" in l)
        self.assertLess(plus, star)

    def test_parentheses_change_the_diagram(self):
        lines = draw(expr("(2 + 3) * 4")).split("\n")
        plus = next(i for i, l in enumerate(lines) if "+" in l)
        star = next(i for i, l in enumerate(lines) if "*" in l)
        self.assertLess(star, plus)

    def test_diagram_of_a_single_leaf(self):
        self.assertEqual(draw(num(7)), "7")

    def test_too_wide_diagram_falls_back_to_the_indented_tree(self):
        program = parse_source("let v = [" + ", ".join(f"a{i}" for i in range(40)) + "];")
        self.assertIsNone(draw(program.statements[0]))
        text = format_program_diagram(program)
        self.assertIn("too wide to draw", text)
        self.assertIn("DeclarationNode", text)

    def test_program_diagram_has_one_section_per_statement(self):
        text = format_program_diagram(parse_source("let x = 1;\nprint(x);"))
        self.assertIn("Statement 1 (line 1):", text)
        self.assertIn("Statement 2 (line 2):", text)

    def test_every_valid_example_can_be_drawn(self):
        for path in sorted((ROOT / "test_inputs").glob("test*.em")):
            if "invalid" in path.name:
                continue
            with self.subTest(path.name):
                result = self.run_cli(str(path), "--diagram")
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertIn("Statement 1", result.stdout)

    def test_flag_may_come_before_the_file(self):
        path = str(ROOT / "test_inputs" / "test1_precedence.em")
        self.assertEqual(self.run_cli("--diagram", path).stdout,
                         self.run_cli(path, "--diagram").stdout)

    def test_diagram_flag_still_reports_errors(self):
        result = self.run_cli(str(ROOT / "test_inputs" / "test7_invalid_missing_expression.em"),
                              "--diagram")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Syntax error at line 1, column 9", result.stdout)
        result = self.run_cli("nope.em", "--diagram")
        self.assertEqual(result.returncode, 1)
        self.assertIn("'nope.em' was not found", result.stdout)

    def test_default_output_is_still_the_indented_tree(self):
        result = self.run_cli(str(ROOT / "test_inputs" / "test1_precedence.em"))
        self.assertTrue(result.stdout.startswith("ProgramNode"))


class TestTreeFormat(unittest.TestCase):
    def test_format_tree(self):
        tree = parse_source("let x = 1 + 2;")
        self.assertEqual(format_tree(tree), "\n".join([
            "ProgramNode",
            "  statements[0]: DeclarationNode name='x'",
            "    value: BinaryOpNode operator='+'",
            "      left: NumberNode value=1",
            "      right: NumberNode value=2",
        ]))


if __name__ == "__main__":
    unittest.main()
