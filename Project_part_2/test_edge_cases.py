import subprocess
import sys
import unittest
from pathlib import Path

from lexer import Lexer, LexerError
from token_definitions import TokenType


class TestLexicalRules(unittest.TestCase):
    def names(self, source):
        return [t.token_type.name for t in Lexer(source).tokenize()]

    def test_all_keywords_and_boundaries(self):
        words = 'let print if else while for func return true false and or not'
        self.assertEqual(self.names(words), [s.upper() for s in words.split()] + ['EOF'])
        self.assertEqual(self.names('letter functionName trueValue Let x_2 function'),
                         ['IDENTIFIER'] * 6 + ['EOF'])

    def test_all_symbols_longest_match(self):
        self.assertEqual(self.names('== != <= >= = < > + - * / ( ) { } [ ] , ;'),
                         ['EQUAL_EQUAL', 'NOT_EQUAL', 'LESS_EQUAL', 'GREATER_EQUAL',
                          'ASSIGN', 'LESS', 'GREATER', 'PLUS', 'MINUS', 'MULTIPLY',
                          'DIVIDE', 'LEFT_PAREN', 'RIGHT_PAREN', 'LEFT_BRACE',
                          'RIGHT_BRACE', 'LEFT_BRACKET', 'RIGHT_BRACKET', 'COMMA',
                          'SEMICOLON', 'EOF'])
        self.assertEqual(self.names('x==y'), ['IDENTIFIER', 'EQUAL_EQUAL', 'IDENTIFIER', 'EOF'])

    def test_numbers_and_unary_minus(self):
        tokens = Lexer('-10 0.25 98.6 007').tokenize()
        self.assertEqual([(t.token_type.name, t.lexeme) for t in tokens],
                         [('MINUS', '-'), ('INTEGER', '10'), ('DECIMAL', '0.25'),
                          ('DECIMAL', '98.6'), ('INTEGER', '007'), ('EOF', '')])

    def test_malformed_decimals(self):
        for source, column in [('.5', 1), ('5.', 2), ('1.2.3', 4)]:
            with self.subTest(source=source), self.assertRaises(LexerError) as caught:
                Lexer(source).tokenize()
            self.assertEqual(str(caught.exception),
                             f"Lexical error at line 1, column {column}: invalid character '.'")

    def test_comments_and_positions(self):
        tokens = Lexer('// ignored @\n\tlet x=2; // end\nprint(x);').tokenize()
        self.assertEqual([(t.lexeme, t.line, t.column) for t in tokens],
                         [('let', 2, 2), ('x', 2, 6), ('=', 2, 7), ('2', 2, 8),
                          (';', 2, 9), ('print', 3, 1), ('(', 3, 6), ('x', 3, 7),
                          (')', 3, 8), (';', 3, 9), ('', 3, 10)])

    def test_line_endings(self):
        for newline in ['\n', '\r\n', '\r']:
            with self.subTest(newline=newline):
                tokens = Lexer('x// comment' + newline + 'y').tokenize()
                self.assertEqual([(t.lexeme, t.line, t.column) for t in tokens],
                                 [('x', 1, 1), ('y', 2, 1), ('', 2, 2)])

    def test_empty_whitespace_and_comment_at_eof(self):
        for source, location in [('', (1, 1)), (' \t\n', (2, 1)), ('// @', (1, 5))]:
            tokens = Lexer(source).tokenize()
            self.assertEqual(len(tokens), 1)
            self.assertEqual(tokens[0].token_type, TokenType.EOF)
            self.assertEqual((tokens[0].line, tokens[0].column), location)

    def test_invalid_characters(self):
        for source, column, char in [('_name', 1, '_'), ('é', 1, 'é'), ('١', 1, '١'),
                                     ('a²', 2, '²'), ('!', 1, '!'), ('\0', 1, '\0'),
                                     ('let x = 10 @ 5;', 12, '@')]:
            with self.subTest(source=source), self.assertRaises(LexerError) as caught:
                Lexer(source).tokenize()
            self.assertEqual(str(caught.exception),
                             f'Lexical error at line 1, column {column}: invalid character {char!r}')

    def test_repeated_scan_has_one_eof(self):
        lexer = Lexer('x')
        self.assertEqual(lexer.tokenize(), lexer.tokenize())
        self.assertEqual(len(lexer.tokens), 2)

    def test_for_boolean_program(self):
        source = 'for (let i = 0; i <= 5; i = i + 1) { print(not false or true and i == 2); }'
        self.assertEqual(self.names(source), [
            'FOR', 'LEFT_PAREN', 'LET', 'IDENTIFIER', 'ASSIGN', 'INTEGER', 'SEMICOLON',
            'IDENTIFIER', 'LESS_EQUAL', 'INTEGER', 'SEMICOLON', 'IDENTIFIER', 'ASSIGN',
            'IDENTIFIER', 'PLUS', 'INTEGER', 'RIGHT_PAREN', 'LEFT_BRACE', 'PRINT',
            'LEFT_PAREN', 'NOT', 'FALSE', 'OR', 'TRUE', 'AND', 'IDENTIFIER',
            'EQUAL_EQUAL', 'INTEGER', 'RIGHT_PAREN', 'SEMICOLON', 'RIGHT_BRACE', 'EOF'])

    def test_cli(self):
        root = Path(__file__).resolve().parent
        cases = [([], 1, 'Usage:'), (['missing_file.em'], 1, 'was not found'),
                 (['test_inputs/test1_declaration.em'], 0, 'EOF'),
                 (['test_inputs/test5_invalid.em'], 1, "column 12: invalid character '@'")]
        for args, code, message in cases:
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(root / 'lexer.py'), *args],
                                        cwd=root, capture_output=True, text=True)
                self.assertEqual(result.returncode, code)
                self.assertIn(message, result.stdout)
                self.assertEqual(result.stderr, '')


if __name__ == '__main__':
    unittest.main()
