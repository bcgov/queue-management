#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
api_dir="$(cd "${script_dir}/.." && pwd)"

cd "${api_dir}"
uv run pytest app/tests -m integration -q \
  --override-ini "addopts=--strict-markers" \
  --require-integration-db
