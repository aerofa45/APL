# Verification results

Executed on September 27, 2026 with the bundled Python runtime.

| Check | Result |
|---|---|
| Part 2 unittest discovery | 17 passed |
| Part 3 unittest discovery | 62 passed |
| Part 4 unittest discovery | 21 passed (including parameterized error cases) |
| Successful CLI programs | 8/8 matched independently specified expected output |
| Runtime-error CLI programs | 3/3 matched expected stderr and exit status 1 |

All 100 automated tests passed. The example verifier also checked that successful
programs exited 0 with empty stderr and the three error programs exited 1 with
empty stdout. Actual output is preserved in `actual/`.

Run `python -m unittest discover -v` separately inside each part's directory,
then `python verify_examples.py` inside Part 4 to reproduce these checks.
Tests were executed by Codex; group members should record their own review and
verification in CONTRIBUTIONS.md before submitting.
