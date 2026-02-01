#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v bats &>/dev/null; then
    echo "Error: bats-core is required" >&2
    echo "Install: brew install bats-core (macOS) or apt install bats (Linux)" >&2
    exit 1
fi

echo "Running intervals-icu API tests..."
echo "=================================="
bats "$SCRIPT_DIR/test_api.bats"
echo ""
echo "All tests passed!"
