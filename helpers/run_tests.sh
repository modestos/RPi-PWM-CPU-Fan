#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke test..."
python3 test/smoke_test.py
echo "All tests passed."
