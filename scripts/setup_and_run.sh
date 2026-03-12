#!/usr/bin/env bash
set -euo pipefail

python -m pip install -e .[dev]
python -m app.init_db
pytest -q

echo "Starting server on 0.0.0.0:8000 ..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
