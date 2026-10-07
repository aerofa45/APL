# Final verification - October 6, 2026
Bundled Python on Windows.

| Check | Result |
|---|---|
| Automated suite | 38 passed: 30 inherited and 8 new |
| Success programs | 18/18 exact stdout, exit 0, empty stderr |
| Error programs | 5/5 exact stderr, exit 1, empty stdout |
| Error stages | lexical, syntax, runtime |
| Diagram regressions | break, continue and programs 14-16 passed |
| Precedence | output 14/20 and multiplication nested inside addition |
| Fresh ZIP extraction | same suite and all 23 program checks passed |

~~~bash
python -m unittest discover -v
python verify_examples.py
~~~
Tests were run by Codex. Members should record independent verification only
after performing it. Passing checks do not prove correctness for every input.
