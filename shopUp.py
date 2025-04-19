#!/usr/bin/env python3
import os
import subprocess
import sys

from config import OUTPUT_DIR

def run_index(python):
    print("[shopUp] Generating main.json…")
    result = subprocess.run(
        [python, "index.py"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"[shopUp] index.py failed: {result.stderr.strip()}")
        sys.exit(result.returncode)
    print("[shopUp] index.py completed successfully")

def run_encrypt(python):
    print("[shopUp] Encrypting to sh.tfl…")
    input_file = os.path.join(OUTPUT_DIR, "main.json")
    output_file = os.path.join(OUTPUT_DIR, "sh.tfl")
    result = subprocess.run(
        [
            python, "encrypt.py",
            "--zstd", "-k", "public.key",
            "-i", input_file,
            "-o", output_file
        ],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"[shopUp] encrypt.py failed: {result.stderr.strip()}")
        sys.exit(result.returncode)
    print("[shopUp] encrypt.py completed successfully")

def main():
    python = sys.executable
    step = sys.argv[1] if len(sys.argv) > 1 else "all"

    if step == "all":
        run_index(python)
        run_encrypt(python)
    elif step == "index":
        run_index(python)
    elif step == "encrypt":
        run_encrypt(python)
    else:
        print('Usage: shopUp.py [all|index|encrypt]')
        sys.exit(1)

if __name__ == "__main__":
    main()