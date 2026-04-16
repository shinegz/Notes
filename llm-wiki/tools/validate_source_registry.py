#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Backward-compatible entry: runs `source_registry_cli.py validate`."""

from __future__ import annotations

import sys
from pathlib import Path

_tools = Path(__file__).resolve().parent
if str(_tools) not in sys.path:
    sys.path.insert(0, str(_tools))

import source_registry_cli  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(source_registry_cli.main(["validate"] + sys.argv[1:]))
