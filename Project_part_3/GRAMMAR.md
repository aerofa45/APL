# Emerald Syntactic Grammar (Part 3, updated)

This is the Part 1 BNF/EBNF, kept unchanged so that Parts 1, 2 and 3 agree.
Part 3 adds no new syntax. It only records how each rule is parsed and which
AST node each rule builds. `{ P }` is zero or more, `[ P ]` is optional, `|`
separates alternatives, and quoted text is a token. The lexical rules
(identifiers, numbers, keywords, comments) are in
`../Project_part_2/UPDATED_GRAMMAR.md`.

## Grammar

```
<program>              ::= { <statement> }

<statement>            ::= <declaration> | <assignment> | <print-statement>
                         | <if-statement> | <while-statement> | <for-statement>
                         | <function-definition> | <return-statement>
                         | <expression-statement> | <block>

<block>                ::= "{" { <statement> } "}"
<declaration>          ::= "let" <identifier> "=" <expression> ";"
<assignment>           ::= <identifier> [ "[" <expression> "]" ] "=" <expression> ";"
<print-statement>      ::= "print" "(" <expression> ")" ";"
<if-statement>         ::= "if" "(" <expression> ")" <block> [ "else" <block> ]
<while-statement>      ::= "while" "(" <expression> ")" <block>
<for-statement>        ::= "for" "(" <for-init> ";" <expression> ";" <for-update> ")" <block>
<for-init>             ::= "let" <identifier> "=" <expression>
                         | <identifier> "=" <expression>
<for-update>           ::= <identifier> [ "[" <expression> "]" ] "=" <expression>
<function-definition>  ::= "func" <identifier> "(" [ <parameter-list> ] ")" <block>
<parameter-list>       ::= <identifier> { "," <identifier> }
<return-statement>     ::= "return" [ <expression> ] ";"
<expression-statement> ::= <expression> ";"

<expression>           ::= <logical-or>
<logical-or>           ::= <logical-and> { "or" <logical-and> }
<logical-and>          ::= <equality> { "and" <equality> }
<equality>             ::= <comparison> { ( "==" | "!=" ) <comparison> }
<comparison>           ::= <arith-expr> { ( "<" | ">" | "<=" | ">=" ) <arith-expr> }
<arith-expr>           ::= <term> { ( "+" | "-" ) <term> }
<term>                 ::= <factor> { ( "*" | "/" ) <factor> }
<factor>               ::= <unary> | <function-call> | <array-literal> | <array-access>
                         | <number> | <identifier> | "true" | "false"
                         | "(" <expression> ")"
<unary>                ::= ( "-" | "not" ) <factor>
<function-call>        ::= <identifier> "(" [ <argument-list> ] ")"
<argument-list>        ::= <expression> { "," <expression> }
<array-literal>        ::= "[" [ <expression> { "," <expression> } ] "]"
<array-access>         ::= <identifier> "[" <expression> "]"
```

## Grammar rule to AST node

| Grammar rule | AST node | Fields |
|---|---|---|
| program | ProgramNode | statements |
| block | BlockNode | statements |
| declaration | DeclarationNode | name, value |
| assignment, for-init, for-update | AssignmentNode | target (VariableNode or IndexNode), value |
| print-statement | PrintNode | value |
| if-statement | IfNode | condition, then_branch, else_branch |
| while-statement | WhileNode | condition, body |
| for-statement | ForNode | init, condition, update, body |
| function-definition | FunctionNode | name, parameters, body |
| return-statement | ReturnNode | value (may be empty) |
| expression-statement | ExpressionStatementNode | expression |
| logical, equality, comparison, arithmetic levels | BinaryOpNode | operator, left, right |
| unary | UnaryOpNode | operator, operand |
| number | NumberNode | value (int or float) |
| true, false | BooleanNode | value |
| identifier used as a value | VariableNode | name |
| function-call | CallNode | name, arguments |
| array-literal | ArrayNode | elements |
| array-access | IndexNode | name, index |

The Part 3 task requires numbers, variables, arithmetic and parenthesized
expressions, assignments, print statements and multiple statements. Those map
to NumberNode, VariableNode, BinaryOpNode, AssignmentNode/DeclarationNode,
PrintNode and ProgramNode. The remaining rules are the rest of the Emerald
grammar from Part 1, so the parser accepts every program that Part 1 defines.

## Precedence and associativity

From lowest to highest: `or`, `and`, `== !=`, `< > <= >=`, `+ -`, `* /`,
unary `- not`. Parentheses, function calls and array indexing bind tightest.
Every binary level is left-associative. Each nonterminal is one method in
`emerald_parser.py`, and the six binary levels share one `binary_level`
helper. Precedence comes from the order of the methods: an operator that
binds tighter is parsed by a method called from deeper in the chain.

Unary operators apply to a `<factor>`, so `-a * b` is `(-a) * b` and
`not a == b` is `(not a) == b`.

## Parsing decisions

- **Assignment or expression statement.** Both can start with an identifier,
  so the parser reads an expression first. If `=` follows, the expression must
  have been written as `name` or `name[expr]`. Otherwise the parser reports
  `invalid assignment target` (for example `x + y = 3;`, `5 = 1;`, `(x) = 1;`).
- **`else` takes a block only.** The grammar has no `else if`; write
  `else { if (...) { ... } }`.
- **Indexing applies to a name only.** `a[0]` is valid; `a[0][1]` and
  `f(1)[0]` are not in the grammar and produce a syntax error.
- **Function definitions are statements**, so they may appear inside blocks.
- **`return` at top level is accepted.** Whether it is meaningful is a
  semantic question, not a syntactic one.
- **Not checked by the parser:** declared-before-use, duplicate names, scoping,
  argument counts, types and array bounds.

## Syntax errors

The parser stops at the first error and reports
`Syntax error at line L, column C: expected <what>, found <token>`. The
position is that of the token the parser could not accept, so a missing `;`
is reported at the start of the next token (or at end of input). For
`let x = ;` the message is
`Syntax error at line 1, column 9: expected expression, found ';'`.
Lexical errors from the Part 2 lexer are reported unchanged.
