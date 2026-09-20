"""Run every example input through the parser and save the actual CLI output."""
from pathlib import Path
import re
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    (root / "outputs").mkdir(exist_ok=True)
    inputs = sorted((root / "test_inputs").glob("test*.em"),
                    key=lambda p: int(re.match(r"test(\d+)_", p.name).group(1)))
    for path in inputs:
        result = subprocess.run([sys.executable, str(root / "emerald_parser.py"), str(path)],
                                capture_output=True, text=True)
        expected = 1 if "invalid" in path.name else 0
        if result.returncode != expected:
            raise RuntimeError(f"Unexpected exit status for {path.name}: {result.stdout}{result.stderr}")
        output = result.stdout + result.stderr
        if not output.strip():
            raise RuntimeError(f"No output for {path.name}")
        (root / "outputs" / (path.stem.split("_")[0] + "_output.txt")).write_text(
            output, encoding="utf-8")
        print(f"{path.name}: expected exit {expected}; output saved")


if __name__ == "__main__":
    main()
