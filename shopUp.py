# shopUp.py
import os
import subprocess
import sys
from config import OUTPUT_DIR

def main():
    # Use the same Python interpreter that’s running this script
    python = sys.executable
    step = sys.argv[1] if len(sys.argv) > 1 else ''

    if step == 'index':
        # Run index.py
        index_cmd = [python, 'index.py']
        proc = subprocess.Popen(index_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if proc.returncode != 0:
            print(f'index.py failed with error: {err.decode()}')
        else:
            print('index.py completed successfully')

    elif step == 'encrypt':
        # Run encrypt.py
        input_file = os.path.join(OUTPUT_DIR, "main.json")
        output_file = "sh.tfl"
        encrypt_cmd = [
            python, 'encrypt.py',
            '--zstd', '-k', 'public.key',
            '-i', input_file,
            '-o', os.path.join(OUTPUT_DIR, output_file)
        ]
        proc = subprocess.Popen(encrypt_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if proc.returncode != 0:
            print(f'encrypt.py failed with error: {err.decode()}')
        else:
            print('encrypt.py completed successfully')

    else:
        print('Please provide a valid step argument: "index" or "encrypt".')

if __name__ == '__main__':
    main()