# AI Use Statement — Part 5

Codex reviewed the existing GitHub interpreter and suggested changes. Some AI assistance by codex was used for part of coding syntax of interpreter.py and also addition to architecture.md was done
All members checked their work and where the confusion happends, checked through the AI, asked questions for external knowledge.

## AI-generated suggestion verified

Codex proposed resetting loop depth to zero on entering a function and restoring
the caller's depth in a finally block. Without that boundary, a break inside a
called function could accidentally exit the caller's loop. This proposal was
verified with test_function_cannot_control_caller_loop for both break and continue.
Both produce a language runtime error, and test_error_restores_context checks
that function and loop counters are restored after a failure.

## Group review

The group did function closures, linked scope dictionaries, and
control-flow signals; and verified against its actual process; This statement discloses the assistance that
actually occurred during this preparation.
