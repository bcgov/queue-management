#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
api_dir="$(cd "${script_dir}/.." && pwd)"

cd "${api_dir}"
uv run pytest app/tests -m smoke -q --override-ini "addopts=--strict-markers"
