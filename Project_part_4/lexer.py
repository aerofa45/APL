from token_definitions import Token, TokenType


class LexerError(Exception):
    pass


KEYWORDS = {
    "let": TokenType.LET,
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "for": TokenType.FOR,
    "func": TokenType.FUNC,
    "return": TokenType.RETURN,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
}


TWO_CHARACTER_TOKENS = {
    "==": TokenType.EQUAL_EQUAL,
    "!=": TokenType.NOT_EQUAL,
    "<=": TokenType.LESS_EQUAL,
    ">=": TokenType.GREATER_EQUAL,
}


ONE_CHARACTER_TOKENS = {
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    "=": TokenType.ASSIGN,
    "<": TokenType.LESS,
    ">": TokenType.GREATER,
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    "[": TokenType.LEFT_BRACKET,
    "]": TokenType.RIGHT_BRACKET,
    ",": TokenType.COMMA,
    ";": TokenType.SEMICOLON,
}


class Lexer:
    def __init__(self, source):
        self.source = source.replace("\r\n", "\n").replace("\r", "\n")
        self.tokens = []
        self.current = 0
        self.line = 1
        self.column = 1

    def is_at_end(self):
        return self.current >= len(self.source)

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def advance(self):
        character = self.source[self.current]
        self.current += 1

        if character == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return character

    def add_token(self, token_type, lexeme, line, column):
        self.tokens.append(
            Token(token_type, lexeme, line, column)
        )


    def skip_whitespace(self):
        while not self.is_at_end() and self.peek() in " \t\r\n":
            self.advance()


    def skip_comment(self):
        while not self.is_at_end() and self.peek() != "\n":
            self.advance()


    def scan_identifier(self):
        start = self.current
        start_line = self.line
        start_column = self.column

        self.advance()

        while (self.peek().isascii() and self.peek().isalnum()) or self.peek() == "_":
            self.advance()

        lexeme = self.source[start:self.current]
        token_type = KEYWORDS.get(
            lexeme,
            TokenType.IDENTIFIER
        )

        self.add_token(
            token_type,
            lexeme,
            start_line,
            start_column
        )


    def scan_number(self):
        start = self.current
        start_line = self.line
        start_column = self.column

        while ("0" <= self.peek() <= "9"):
            self.advance()

        is_decimal = False

        if self.peek() == "." and ("0" <= self.peek_next() <= "9"):
            is_decimal = True
            self.advance()

            while ("0" <= self.peek() <= "9"):
                self.advance()

        lexeme = self.source[start:self.current]

        if is_decimal:
            token_type = TokenType.DECIMAL
        else:
            token_type = TokenType.INTEGER

        self.add_token(
            token_type,
            lexeme,
            start_line,
            start_column
        )


    def tokenize(self):
        """Scan the source afresh; return tokens ending with exactly one EOF."""
        self.tokens = []
        self.current = 0
        self.line = 1
        self.column = 1
        while not self.is_at_end():
            character = self.peek()

            if character in " \t\r\n":
                self.skip_whitespace()
                continue

            if character == "/" and self.peek_next() == "/":
                self.advance()
                self.advance()
                self.skip_comment()
                continue

            if character.isascii() and character.isalpha():
                self.scan_identifier()
                continue

            if "0" <= character <= "9":
                self.scan_number()
                continue

            start_line = self.line
            start_column = self.column

            two_characters = (
                character + self.peek_next()
            )

            if two_characters in TWO_CHARACTER_TOKENS:
                self.advance()
                self.advance()

                self.add_token(
                    TWO_CHARACTER_TOKENS[two_characters],
                    two_characters,
                    start_line,
                    start_column
                )
                continue

            if character in ONE_CHARACTER_TOKENS:
                self.advance()

                self.add_token(
                    ONE_CHARACTER_TOKENS[character],
                    character,
                    start_line,
                    start_column
                )
                continue

            raise LexerError(
                f"Lexical error at line {self.line}, "
                f"column {self.column}: "
                f"invalid character {character!r}"
            )

        self.tokens.append(
            Token(TokenType.EOF, "", self.line, self.column)
        )

        return self.tokens


def tokenize_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        source = file.read()

    lexer = Lexer(source)
    return lexer.tokenize()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python lexer.py <source-file>")
        sys.exit(1)

    try:
        tokens = tokenize_file(sys.argv[1])

        for token in tokens:
            print(token)

    except FileNotFoundError:
        print(f"Error: file {sys.argv[1]!r} was not found.")
        sys.exit(1)

    except LexerError as error:
        print(error)
        sys.exit(1)

    except (OSError, UnicodeError) as error:
        print(f"Error: {error}")
        sys.exit(1)
