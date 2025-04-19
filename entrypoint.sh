#!/bin/sh
set -e

echo "[entrypoint] Regenerating catalog…"
python3 shopUp.py    # default “all” mode: index + encrypt

echo "[entrypoint] Launching server…"
# hand off to CMD (Gunicorn or python3 app.py)
exec "$@"