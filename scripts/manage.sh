#!/usr/bin/env sh
set -eu
aaes_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec "${AAES_PYTHON:-python3}" "$aaes_dir/manage.py" "$@"
