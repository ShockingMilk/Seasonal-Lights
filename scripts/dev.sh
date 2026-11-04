#!/usr/bin/env bash

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

pip install -e .

echo
echo "Development environment ready."
echo
echo "Run:"
echo "  source .venv/bin/activate"
echo "  python -m seasonal_lights.main"
echo
echo "Tests:"
echo "  pytest"