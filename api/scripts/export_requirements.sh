#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
api_dir="$(cd "${script_dir}/.." && pwd)"

cd "${api_dir}"
uv export --frozen --format requirements-txt --no-emit-project --output-file requirements.txt
uv export --frozen --format requirements-txt --no-emit-project --group dev --output-file requirements_dev.txt
