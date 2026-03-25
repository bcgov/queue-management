#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
api_dir="$(cd "${script_dir}/.." && pwd)"

cd "${api_dir}"
python3 -m pytest app/tests -q
