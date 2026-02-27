#!/usr/bin/env bash
# run_tests.sh — run the pytest suite from the project root on Linux / macOS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

source .venv/bin/activate

echo
echo "Running test suite..."
echo

pytest tests/ -v
