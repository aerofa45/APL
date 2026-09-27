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

## Emerald Lexical Rules

Emerald uses 13 reserved keywords. The **Vela** keyword was accidentally included in an earlier version and removed here․ The keyword for has been added to the original 12 reserved words to make it consistent with the Part 1 rule for for-loops․

The statement and expression grammars‚ including operator precedence‚ are the same as in Part 1․ This handout provides lexical information․ Features such as parsing‚ running‚ scope analysis‚ and array bounds analysis are not part of this project․

The statement and expression grammar, including operator precedence, remains unchanged from Part 1. This document describes lexical rules only. Parsing, execution, scope checking, and array bounds checking are not implemented in this project.

### Identifiers and Keywords

A `<letter>` is any ASCII character from `A-Z` or `a-z`, and a `<digit>` is any ASCII character from `0-9`.

Identifiers must begin with a letter. Underscores are allowed only after the first character. Identifiers and keywords are case-sensitive.

`function` is treated as a regular identifier, while `func` is the reserved keyword for function declarations.

Non-ASCII letters and digits are not supported. These rules follow the original Part 1 specification instead of the tutorial's optional leading-underscore rule or Python's broader Unicode identifier rules.

### Tokenization Rules

The lexer follows the **maximal munch** rule, meaning it scans the longest valid token whenever possible.

- Complete identifiers are scanned before checking whether they are keywords.
- Two-character comparison operators are recognized before single-character symbols.
- `//` is recognized as a comment before `/` is treated as division.
- The minus sign (`-`) is always treated as a separate token.

Decimal numbers must contain digits on both sides of the decimal point. Therefore, values such as `.5`, `5.`, and `1.2.3` produce a lexical error when the unsupported dot is encountered.

Strings, exponent notation, block comments, and additional operators are not supported by this grammar.

Adjacent recognizable lexemes are tokenized separately. For example, `12abc` is scanned as separate tokens. Whether such a sequence forms a valid expression is the responsibility of the parser.

### Position Tracking and Errors

Line and column numbering both begin at `1`. A tab increases the column number by one.

`CRLF` and standalone `CR` line endings are normalized to `LF` before scanning, including when the `Lexer` is used directly.

Comments continue until a newline or the end of the file.

A successful scan ends with exactly one `EOF` token. The `EOF` token has an empty lexeme and records the next source position after the final character.

If an unsupported character is encountered, scanning stops immediately at that character and no partial token stream is returned.


File Created and updated By Abir 
