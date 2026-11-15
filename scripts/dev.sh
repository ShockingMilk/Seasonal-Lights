#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$PROJECT_ROOT"

python3 -m venv .venv

source .venv/bin/activate

python -m pip install --upgrade pip

pip install -e ".[dev]"

pytest