# Verification — October 4, 2026

The package was verified using the bundled Python runtime on Windows.

| Check                            | Result                                                      |
| -------------------------------- | ----------------------------------------------------------- |
| Part 5 behavioral suite          | 30 tests passed (21 inherited, 9 new)                       |
| Success programs                 | 17/17 matched expected stdout and exit 0, with empty stderr |
| Runtime-error programs           | 3/3 matched expected stderr and exit 1, with empty stdout   |
| Original Part 2 regression suite | 17 passed                                                   |
| Original Part 3 regression suite | 62 passed                                                   |

The original milestone suites were run separately against their historical source.
Part 5 tests include all nine new programs through test_complete_programs, plus
scope isolation, closures, recursion, and loop-control error cases.
Part 5's exact CLI verifier checks all 20 complete programs.
An initial copying error added a blank line to inherited expected files; those
