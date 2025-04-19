#!/bin/sh
set -e

echo "[entrypoint] Generating main.json…"
python3 shopUp.py index

echo "[entrypoint] Encrypting to sh.tfl…"
python3 shopUp.py encrypt --zstd -k public.key \
    -i data/output/main.json \
    -o data/output/sh.tfl

echo "[entrypoint] Launching server…"
# now hand off to whatever CMD was specified (Gunicorn)
exec "$@"