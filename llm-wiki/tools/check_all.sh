#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# One-shot health check: layout → validate registry → lint wiki.
# Usage: bash tools/check_all.sh [WIKI_ROOT]
set -euo pipefail
ROOT="${1:-.}"
ROOT="$(cd "$ROOT" && pwd)"
DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$DIR/source_registry_cli.py" layout "$ROOT"
python3 "$DIR/source_registry_cli.py" validate "$ROOT"
python3 "$DIR/lint_wiki.py" "$ROOT"
