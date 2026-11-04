#!/usr/bin/env bash

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found."
    echo "Run:"
    echo "  python3 -m venv .venv"
    exit 1
fi

source .venv/bin/activate

python -m seasonal_lights.main