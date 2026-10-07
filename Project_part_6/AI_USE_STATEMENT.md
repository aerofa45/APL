# AI Use Statement - Final Package

OpenAI Codex was used in this conversation to review GitHub, generate substantial
Part 5 code, tests and documentation, explain concepts, and prepare Part 6.
Part 6 assistance included file organization, entry-point integration, a diagram
fix, new regression and example tests, documentation and test execution.
The group contribution record is retained separately. AI-prepared additions
are not claimed here as independently authored student work.

## AI-generated code requiring correction
The earlier Codex-prepared package added BreakNode and ContinueNode but left the
inherited diagram label map unchanged. Program 14 with --diagram raised KeyError
for ContinueNode. During Part 6 preparation Codex added both node labels and
regression tests for break/continue diagrams and CLI diagrams of programs 14-16.
Members should reproduce and explain this actual defect and correction.

## Verification
The automated suite checks behavior and integration. The CLI verifier compares
fixed expected outputs, exit codes and streams, including lexical, syntax and
runtime failures. New cases also check precedence and diagrams. The ZIP was
extracted into a separate directory and verified again. New expected values were
specified before execution. See TEST_RESULTS.md.

## Responsibility
Members should understand the code and discuss tools, assisted tasks, this
correction and verification in the report and recording. Name other AI tools only
if used. Record student review/testing only after it occurs.
