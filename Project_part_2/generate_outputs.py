"""Run all six example inputs and save actual CLI output."""
from pathlib import Path
import subprocess
import sys

def main():
    root = Path(__file__).resolve().parent
    (root / "outputs").mkdir(exist_ok=True)
    for path in sorted((root / "test_inputs").glob("test*.em")):
        result = subprocess.run([sys.executable, str(root / "lexer.py"), str(path)],
                                capture_output=True, text=True)
        expected = 1 if path.name.startswith("test5_") else 0
        if result.returncode != expected:
            raise RuntimeError(f"Unexpected exit status for {path.name}: {result.stderr}")
        output = result.stdout + result.stderr
        if not output.strip():
            raise RuntimeError(f"No output for {path.name}")
        (root / "outputs" / (path.stem.split("_")[0] + "_output.txt")).write_text(
            output, encoding="utf-8")
        print(f"{path.name}: expected exit {expected}; output saved")

if __name__ == "__main__":
    main()
