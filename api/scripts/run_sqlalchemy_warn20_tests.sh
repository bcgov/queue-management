#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
api_dir="$(cd "${script_dir}/.." && pwd)"

cd "${api_dir}"
export SQLALCHEMY_WARN_20=1
uv run pytest app/tests -q \
  -W "error::sqlalchemy.exc.RemovedIn20Warning" \
  -W "error::sqlalchemy.exc.SADeprecationWarning"
