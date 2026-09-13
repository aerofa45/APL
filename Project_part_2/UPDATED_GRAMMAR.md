# Emerald Lexical Grammar

## Keywords

let | print | if | else | while | for | func | return |
true | false | and | or | not

## Identifier

<identifier> ::= <letter>
                 { <letter> | <digit> | "_" }

## Numbers

<number> ::= <integer> | <decimal>

<integer> ::= <digit> { <digit> }

<decimal> ::= <digit> { <digit> }
              "." <digit> { <digit> }

## Arithmetic Operators

+ | - | * | /

## Comparison Operators

== | != | < | > | <= | >=

## Assignment Operator

=

## Delimiters

( | ) | { | } | [ | ] | , | ;

## Whitespace

Spaces, tabs, carriage returns, and newlines separate lexemes
and are ignored by the lexer.

## Comments

A comment begins with // and continues until the end of the line.
Comments are ignored by the lexer.

## Lexical Error

Any character that cannot begin a valid Emerald token produces
a lexical error containing the character's line and column.

## Corrections and relationship to Part 1

Emerald reserves 13 keywords. This corrects the accidental name "Vela"
and adds `for` to the original 12-word table, matching Part 1's for-loop rule.
The statement/expression grammar and precedence from Part 1 are unchanged.
This document specifies lexical rules only; this project does not implement
a parser, execution, scope checking, or array bounds checking.

`<letter>` is ASCII A-Z or a-z; `<digit>` is ASCII 0-9, as in Part 1.
Identifiers must start with a letter; underscores are allowed only afterward.
Names and keywords are case-sensitive. `function` is an identifier; `func`
is the function keyword. Non-ASCII letters/digits are not accepted.
This preserves Part 1 rather than adopting the pasted tutorial's optional
leading-underscore extension or Python's broader Unicode character classes.

The scanner uses maximal munch: scan full identifiers before keyword lookup,
recognize two-character comparisons before single-character symbols, and
recognize `//` before division. A minus sign is a separate token.
Decimals require digits on both sides of the dot; `.5`, `5.`, and `1.2.3`
produce a lexical error at the unsupported dot. Strings, exponent notation,
block comments, and additional operators are not defined by this grammar.
Adjacent recognizable lexemes (such as `12abc`) are tokenized separately;
whether their sequence is a valid expression is a parser concern.

Line and column numbers start at 1. Tabs advance one column. CRLF and lone
CR are normalized to LF before scanning, including when using Lexer directly.
Comments end at a newline or EOF. A successful scan ends with exactly one EOF
token with an empty lexeme and the next source position. Invalid input stops
at the first unsupported character, without returning a partial token stream.
