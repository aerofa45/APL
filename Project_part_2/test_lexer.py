import unittest

from lexer import Lexer, LexerError
from token_definitions import TokenType


class TestEmeraldLexer(unittest.TestCase):
    def token_types(self, source):
        tokens = Lexer(source).tokenize()
        return [token.token_type for token in tokens]

    def test_variable_declaration(self):
        result = self.token_types("let x = 10;")

        expected = [
            TokenType.LET,
            TokenType.IDENTIFIER,
            TokenType.ASSIGN,
            TokenType.INTEGER,
            TokenType.SEMICOLON,
            TokenType.EOF,
        ]

        self.assertEqual(result, expected)

    def test_arithmetic_expression(self):
        result = self.token_types(
            "let result = (10 + 5) * 2;"
        )

        self.assertIn(TokenType.PLUS, result)
        self.assertIn(TokenType.MULTIPLY, result)
        self.assertIn(TokenType.LEFT_PAREN, result)
        self.assertIn(TokenType.RIGHT_PAREN, result)

    def test_print_statement(self):
        result = self.token_types("print(result);")

        expected = [
            TokenType.PRINT,
            TokenType.LEFT_PAREN,
            TokenType.IDENTIFIER,
            TokenType.RIGHT_PAREN,
            TokenType.SEMICOLON,
            TokenType.EOF,
        ]

        self.assertEqual(result, expected)

    def test_control_structure(self):
        source = """
        if (x >= 5) {
            print(x);
        } else {
            x = x + 1;
        }
        """

        result = self.token_types(source)

        self.assertIn(TokenType.IF, result)
        self.assertIn(TokenType.ELSE, result)
        self.assertIn(TokenType.GREATER_EQUAL, result)
        self.assertIn(TokenType.LEFT_BRACE, result)
        self.assertIn(TokenType.RIGHT_BRACE, result)

    def test_invalid_character(self):
        with self.assertRaises(LexerError) as context:
            Lexer("let x = 10 @ 5;").tokenize()

        self.assertIn(
            "invalid character '@'",
            str(context.exception)
        )

    def test_function_and_array(self):
        source = """
        func add(a, b) {
            return a + b;
        }

        let values = [1, 2, 3];
        """

        result = self.token_types(source)

        self.assertIn(TokenType.FUNC, result)
        self.assertIn(TokenType.RETURN, result)
        self.assertIn(TokenType.COMMA, result)
        self.assertIn(TokenType.LEFT_BRACKET, result)
        self.assertIn(TokenType.RIGHT_BRACKET, result)


if __name__ == "__main__":
    unittest.main()
