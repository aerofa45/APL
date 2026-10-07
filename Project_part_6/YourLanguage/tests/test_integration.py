"""Final entry-point, error and diagram regression checks."""
from pathlib import Path
import subprocess
import sys
import unittest
from parser import parse_source
from ast_diagram import format_program_diagram

ROOT = Path(__file__).resolve().parent.parent

class FinalIntegrationTests(unittest.TestCase):
    def cli(self, file, *args):
        return subprocess.run([sys.executable, str(ROOT / file), *args],
                              cwd=ROOT, capture_output=True, text=True)

    def test_break_diagram(self):
        self.assertIn("break", format_program_diagram(parse_source("while(true){break;}")))

    def test_continue_diagram(self):
        self.assertIn("continue", format_program_diagram(parse_source("for(let i=0;i<2;i=i+1){continue;}")))

    def test_diagram_cli_on_extension_programs(self):
        for name in ("14_for_continue", "15_while_break", "16_nested_loops"):
            with self.subTest(name=name):
                r = self.cli("parser.py", f"tests/programs/{name}.em", "--diagram")
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(r.stderr, "")
                self.assertIn("Statement", r.stdout)

    def test_main_entry_point(self):
        r = self.cli("main.py", "tests/programs/09_function_add.em")
        self.assertEqual((r.returncode, r.stdout, r.stderr), (0, "30\n", ""))

    def test_main_usage(self):
        r = self.cli("main.py")
        self.assertEqual(r.returncode, 2)
        self.assertIn("usage:", r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_error_stages_and_locations(self):
        for name in ("error_lexical", "error_syntax", "error_division"):
            with self.subTest(name=name):
                r = self.cli("main.py", f"tests/error_programs/{name}.em")
                expected = (ROOT / "tests/expected" / f"{name}.txt").read_text()
                self.assertEqual((r.returncode, r.stdout, r.stderr), (1, "", expected))

    def test_precedence_outputs(self):
        r = self.cli("main.py", "tests/programs/18_precedence.em")
        self.assertEqual((r.returncode, r.stdout, r.stderr), (0, "14\n20\n", ""))

    def test_precedence_ast(self):
        expression = parse_source("print(2 + 3 * 4);").statements[0].value
        self.assertEqual(expression.operator, "+")
        self.assertEqual(expression.right.operator, "*")

if __name__ == "__main__":
    unittest.main()
