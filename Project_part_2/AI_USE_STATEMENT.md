# AI Use Statement

OpenAI Codex was used to read the supplied Part 1 Emerald language document
and the user-provided implementation instructions, generate and adapt the
Python lexer and token definitions, create automated tests and documentation,
run verification, save example outputs, and package the project.

The implementation builds directly on the AI-assisted code supplied in the
instructions. Codex adapted it to preserve Part 1's ASCII, letter-first
identifier rule, handle line endings consistently, and report file errors.
The original Part 1 document was provided as the language specification.

### AI USE STATEMENT

**AI Tool(s) Used:**

ChatGPT and OpenAI Codex.

**How did your group use AI for this project milestone?**

Our group used AI to help implement the Emerald lexer based on our Part 1 grammar. AI helped generate and explain Python code, organize token categories, suggest test cases, and prepare documentation and running instructions.

**Which project components received AI assistance?**

AI assisted with the lexer implementation, token definitions, automated tests, sample test inputs, saved outputs, README, and updated lexical grammar.

**Describe at least one AI-generated suggestion, explanation, or code segment that your group modified, corrected, rejected, or improved.**

Our group changed the AI-generated test inputs, including the arithmetic expression, and added a print statement to examine the resulting tokens. We also used a revised identifier-recognition section in `lexer.py` that requires identifiers to begin with an ASCII letter while allowing underscores afterward. This made the lexer consistent with our Part 1 grammar.

**How did your group test or independently verify AI-assisted work?**

We changed sample inputs and used the lexer’s output to check how those changes affected the token sequence. Codex also ran 17 automated tests, which all passed, and checked six sample programs. These checks covered declarations, arithmetic, printing, control structures, functions, arrays, and invalid input. The invalid-input test correctly reported an error for `@`.

**What did your group learn from using AI during this milestone?**

We learned how a lexer separates source code into lexemes and assigns token categories. We also learned how to edit test inputs, run the tests, and examine token output. Reviewing the implementation helped us understand why longer operators must be recognized first and why generated code needs to match our language grammar.

**The purpose of this statement is to document how AI contributed to your development process and how your group evaluated its output.**
