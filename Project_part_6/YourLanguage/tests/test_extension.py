import io
import unittest
from interpreter import Interpreter
from environment import EmeraldRuntimeError
from parser import parse_source, ParseError
from lexer import Lexer
from token_definitions import TokenType
from ast_nodes import BreakNode, ContinueNode

class ExtensionTests(unittest.TestCase):
    def run_source(self, source):
        output = io.StringIO()
        runner = Interpreter(output)
        runner.run(source)
        return output.getvalue(), runner

    def test_tokens_and_ast_positions(self):
        tokens = Lexer("break; continue;").tokenize()
        self.assertEqual(tokens[0].token_type, TokenType.BREAK)
        self.assertEqual(tokens[2].token_type, TokenType.CONTINUE)
        nodes = parse_source("break; continue;").statements
        self.assertIsInstance(nodes[0], BreakNode)
        self.assertIsInstance(nodes[1], ContinueNode)
        self.assertEqual((nodes[1].line, nodes[1].column), (1, 8))

    def test_semicolon_required(self):
        for source in ("break", "continue"):
            with self.subTest(source=source), self.assertRaises(ParseError):
                parse_source(source)

    def test_controls_outside_loop(self):
        for source in ("break;", "continue;"):
            with self.subTest(source=source), self.assertRaisesRegex(EmeraldRuntimeError, "line 1, column 1"):
                self.run_source(source)

    def test_function_cannot_control_caller_loop(self):
        for control in ("break", "continue"):
            with self.subTest(control=control), self.assertRaisesRegex(EmeraldRuntimeError, "outside a loop"):
                self.run_source("func f(){" + control + ";} while(true){f();}")

    def test_continue_while(self):
        output, runner = self.run_source("let i=0; while(i<4){i=i+1; if(i==2){continue;} print(i);}")
        self.assertEqual(output, "1\n3\n4\n")
        self.assertEqual(runner.loop_depth, 0)

    def test_return_restores_loop_context(self):
        output, runner = self.run_source("func f(){while(true){return 7;}} for(let i=0;i<3;i=i+1){print(f()); break;}")
        self.assertEqual(output, "7\n")
        self.assertEqual((runner.loop_depth, runner.call_depth), (0,0))

    def test_error_restores_context(self):
        runner = Interpreter(io.StringIO())
        with self.assertRaises(EmeraldRuntimeError):
            runner.run("func f(){while(true){print(1/0);}} while(true){f();}")
        self.assertEqual((runner.loop_depth, runner.call_depth), (0,0))
        with self.assertRaisesRegex(EmeraldRuntimeError, "outside a loop"):
            runner.run("break;")

    def test_local_variables_do_not_escape(self):
        with self.assertRaisesRegex(EmeraldRuntimeError, "undefined variable 'local'"):
            self.run_source("func f(){let local=3; return local;} f(); print(local);")

    def test_nested_continue(self):
        output, _ = self.run_source("let n=0; for(let i=0;i<2;i=i+1){for(let j=0;j<3;j=j+1){if(j==1){continue;} n=n+1;}} print(n);")
        self.assertEqual(output, "4\n")

if __name__ == "__main__":
    unittest.main()
