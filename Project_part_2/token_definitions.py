from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    # Keywords
    LET = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    FUNC = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    # Identifiers and numeric literals
    IDENTIFIER = auto()
    INTEGER = auto()
    DECIMAL = auto()

    # Arithmetic operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()

    # Comparison operators
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    # Assignment
    ASSIGN = auto()

    # Delimiters
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()

    EOF = auto()


@dataclass
class Token:
    token_type: TokenType
    lexeme: str
    line: int
    column: int

    def __str__(self):
        if self.lexeme:
            return (
                f"{self.token_type.name}({self.lexeme!r}) "
                f"at line {self.line}, column {self.column}"
            )

        return (
            f"{self.token_type.name} "
            f"at line {self.line}, column {self.column}"
        )
