"""Execute submission programs and compare actual output to fixed expectations."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    actual_dir = ROOT / 'actual'
    actual_dir.mkdir(exist_ok=True)
    results = []
    for folder, expected_status in [('programs', 0), ('error_programs', 1)]:
        for source in sorted((ROOT / folder).glob('*.em')):
            result = subprocess.run([sys.executable, str(ROOT / 'interpreter.py'), str(source)],
                                    capture_output=True, text=True)
            actual = result.stdout if expected_status == 0 else result.stderr
            unexpected = result.stderr if expected_status == 0 else result.stdout
            expected = (ROOT / 'expected' / (source.stem + '.txt')).read_text(encoding='utf-8')
            (actual_dir / (source.stem + '.txt')).write_text(actual, encoding='utf-8')
            passed = actual == expected and result.returncode == expected_status and not unexpected
            results.append(passed)
            print(f"{'PASS' if passed else 'FAIL'} {source.name}: exit {result.returncode}")
    print(f'{sum(results)}/{len(results)} programs matched expected output and exit status')
    return 0 if results and all(results) else 1


if __name__ == '__main__':
    sys.exit(main())

