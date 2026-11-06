#!/usr/bin/env sh
set -eu
case "${1:-}" in
  codex|claude) target=$1 ;;
  *) echo 'Usage: sh scripts/install.sh codex|claude [all|skill-name] [install-path]' >&2; exit 2 ;;
esac
if [ "$#" -gt 3 ]; then
  echo 'Too many arguments' >&2
  exit 2
fi
skill=${2:-all}
install_path=${3:-}
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
set -- install --target "$target"
if [ "$skill" != all ]; then set -- "$@" --skill "$skill"; fi
if [ -n "$install_path" ]; then set -- "$@" --destination "$install_path"; fi
exec sh "$here/manage.sh" "$@"
