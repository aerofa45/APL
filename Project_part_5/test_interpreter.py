"""Behavioral tests for execution, scope, runtime failures, and CLI."""
import io
from pathlib import Path
import subprocess
import sys
import unittest

from interpreter import Interpreter
from environment import EmeraldRuntimeError

ROOT = Path(__file__).resolve().parent


class InterpreterTests(unittest.TestCase):
    def run_source(self, source, **options):
        output = io.StringIO()
        runner = Interpreter(output, **options)
        env = runner.run(source)
        return output.getvalue(), env

    def test_arithmetic_and_assignment(self):
        output, env = self.run_source('let x = 10; let y = x + 5; x = y - 2; print(x); print(2 + 3 * 4); print((2 + 3) * 4); print(9 / 2);')
        self.assertEqual(output, '13\n14\n20\n4.5\n')
        self.assertEqual(env.get('y'), 15)

    def test_all_comparisons(self):
        output, _ = self.run_source('print(2 == 2.0); print(2 != 3); print(2 < 3); print(3 > 2); print(2 <= 2); print(2 >= 2);')
        self.assertEqual(output, 'true\n' * 6)

    def test_if_else_and_no_else(self):
        output, _ = self.run_source('if (true) {print(1);} else {print(0);} if (false) {print(0);} else {print(2);} if (false) {print(9);}')
        self.assertEqual(output, '1\n2\n')

    def test_while_and_zero_iterations(self):
        output, env = self.run_source('let x=1; while(x<=5){print(x); x=x+1;} while(false){print(99);}')
        self.assertEqual(output, '1\n2\n3\n4\n5\n')
        self.assertEqual(env.get('x'), 6)

    def test_scope_shadowing_and_outer_assignment(self):
        output, env = self.run_source('let x=10; {let x=20; x=x+1; print(x);} {x=x+1;} print(x);')
        self.assertEqual(output, '21\n11\n')
        self.assertEqual(env.get('x'), 11)

    def test_block_variable_does_not_escape(self):
        with self.assertRaisesRegex(EmeraldRuntimeError, "undefined variable 'local'"):
            self.run_source('{let local=1;} print(local);')

    def test_fresh_loop_body_scope(self):
        self.assertEqual(self.run_source('let i=0; while(i<3){let local=i; print(local); i=i+1;}')[0], '0\n1\n2\n')

    def test_short_circuit_and_unary(self):
        output, _ = self.run_source('print(false and missing); print(true or (1/0 == 0)); print(not false); print(-2 * 3);')
        self.assertEqual(output, 'false\ntrue\ntrue\n-6\n')

    def test_for_loop_scope(self):
        output, env = self.run_source('let total=0; for(let i=0;i<4;i=i+1){total=total+i;} print(total);')
        self.assertEqual(output, '6\n')
        with self.assertRaises(EmeraldRuntimeError):
            env.get('i')

    def test_array_read_write_alias(self):
        output, _ = self.run_source('let a=[1,2]; let b=a; b[0]=9; print(a); print(a[1]);')
        self.assertEqual(output, '[9, 2]\n2\n')

    def test_recursive_function(self):
        output, _ = self.run_source('func fact(n){if(n<=1){return 1;} return n*fact(n-1);} print(fact(5));')
        self.assertEqual(output, '120\n')

    def test_lexical_scope_not_caller_scope(self):
        output, _ = self.run_source('let x=10; func read(){return x;} func caller(){let x=99; return read();} print(caller());')
        self.assertEqual(output, '10\n')

    def test_closure_and_return_from_loop(self):
        output, _ = self.run_source('func make(x){func read(){return x;} return read;} let f=make(8); print(f()); func first(){while(true){return 7;}} print(first());')
        self.assertEqual(output, '8\n7\n')

    def test_bare_and_implicit_return(self):
        self.assertEqual(self.run_source('func a(){return;} func b(){} print(a()); print(b());')[0], 'nil\nnil\n')

    def test_runtime_error_cases(self):
        cases = [
            ('print(x);', "undefined variable 'x'"),
            ('x=3;', "undefined variable 'x'"),
            ('print(1/0);', 'division by zero'),
            ('print(true+1);', 'numeric operand required'),
            ('print([1]*2);', 'numeric operand required'),
            ('if(1){}', 'boolean value required'),
            ('print(not 1);', 'boolean value required'),
            ('print(true and 1);', 'boolean value required'),
            ('print(true==1);', 'equality requires'),
            ('let x=1; let x=2;', 'already declared'),
            ('let a=[1]; print(a[-1]);', 'out of bounds'),
            ('let a=[1]; a[1]=2;', 'out of bounds'),
            ('let a=[1]; print(a[0.0]);', 'index must be an integer'),
            ('let a=[1]; print(a[true]);', 'index must be an integer'),
            ('let a=1; print(a[0]);', 'not an array'),
            ('let a=1; a();', 'not callable'),
            ('func f(x){} f();', 'expects 1 arguments'),
            ('func f(x,x){}', 'duplicate function parameter'),
            ('return 1;', 'return outside a function'),
        ]
        for source, message in cases:
            with self.subTest(source=source):
                with self.assertRaisesRegex(EmeraldRuntimeError, message):
                    self.run_source(source)

    def test_error_location(self):
        with self.assertRaisesRegex(EmeraldRuntimeError, 'line 2, column 8: division by zero'):
            self.run_source('let x=0;\nprint(4/x);')

    def test_execution_limit(self):
        with self.assertRaisesRegex(EmeraldRuntimeError, 'execution limit'):
            self.run_source('while(true){}', max_steps=30)

    def test_recursive_limit_is_language_error(self):
        with self.assertRaisesRegex(EmeraldRuntimeError, 'recursion limit'):
            self.run_source('func f(){return f();} f();')

    def test_cyclic_array_print(self):
        self.assertEqual(self.run_source('let a=[0]; a[0]=a; print(a);')[0], '[[...]]\n')

    def test_complete_programs(self):
        for path in sorted((ROOT / 'programs').glob('*.em')):
            with self.subTest(program=path.name):
                expected = (ROOT / 'expected' / (path.stem + '.txt')).read_text()
                self.assertEqual(self.run_source(path.read_text())[0], expected)

    def test_cli_failures(self):
        for args, message in [([], 'usage:'), (['missing.em'], 'No such file'),
                              (['programs/01_variables.em', '--max-steps', '0'], 'must be positive')]:
            result = subprocess.run([sys.executable, str(ROOT / 'interpreter.py'), *args], cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(message, result.stderr)
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
