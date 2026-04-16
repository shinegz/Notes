#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Source registry CLI: validate, match-url, match-file, list, get, deps.

Match logic adapted from llm-wiki-skill scripts/source-registry.sh (match_url / match_file).

Usage:
  python3 source_registry_cli.py validate [WIKI_ROOT]
  python3 source_registry_cli.py match-url <url>
  python3 source_registry_cli.py match-file <path>
  python3 source_registry_cli.py list [--category core|optional|manual]
  python3 source_registry_cli.py get <source_id>
  python3 source_registry_cli.py deps <bundled|install_time|none>
  python3 source_registry_cli.py layout <WIKI_ROOT>
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

EXPECTED_HEADER = [
    "source_id",
    "source_label",
    "source_category",
    "input_mode",
    "match_rule",
    "raw_dir",
    "adapter_name",
    "dependency_name",
    "dependency_type",
    "fallback_hint",
]

CATEGORIES = {"core", "optional", "manual"}
INPUT_MODES = {"url", "file", "text"}
DEP_TYPES = {"none", "bundled", "install_time"}
PLACEHOLDER = "-"


def tools_dir() -> Path:
    return Path(__file__).resolve().parent


def registry_path() -> Path:
    return tools_dir() / "source_registry.tsv"


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def taxonomy_top_shelves(taxonomy_md: Path) -> list[str]:
    """Top-level shelf ids from taxonomy.md table cells like `raw/agent/` (machine-aided layout check)."""
    text = taxonomy_md.read_text(encoding="utf-8")
    found: set[str] = set()
    for line in text.splitlines():
        if not line.strip().startswith("|") or "`raw/" not in line:
            continue
        for m in re.finditer(r"`raw/([a-z0-9-]+)/`", line):
            found.add(m.group(1))
    return sorted(found)


def load_rows(tsv: Path) -> list[dict[str, str]]:
    if not tsv.is_file():
        die(f"missing {tsv}")
    lines = tsv.read_text(encoding="utf-8").splitlines()
    if not lines:
        die("empty source_registry.tsv")
    header = lines[0].split("\t")
    if header != EXPECTED_HEADER:
        die(
            "source_registry.tsv header mismatch\n"
            f"  expected: {EXPECTED_HEADER}\n"
            f"  actual:   {header}"
        )
    rows: list[dict[str, str]] = []
    with tsv.open(newline="", encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f, delimiter="\t"), start=2):
            if any(not (row.get(h) or "").strip() for h in EXPECTED_HEADER):
                die(f"source_registry.tsv line {i}: empty field")
            rows.append({h: (row.get(h) or "").strip() for h in EXPECTED_HEADER})
    return rows


def validate_rows(rows: list[dict[str, str]]) -> None:
    seen_ids: set[str] = set()
    cats: set[str] = set()
    default_rows = 0

    for i, row in enumerate(rows, start=2):
        sid = row["source_id"]
        if sid in seen_ids:
            die(f"source_registry.tsv line {i}: duplicate source_id {sid!r}")
        seen_ids.add(sid)

        cat = row["source_category"]
        if cat not in CATEGORIES:
            die(f"source_registry.tsv line {i}: unknown source_category {cat!r}")
        cats.add(cat)

        im = row["input_mode"]
        if im not in INPUT_MODES:
            die(f"source_registry.tsv line {i}: unknown input_mode {im!r}")

        mr = row["match_rule"]
        if im == "file" and not mr.startswith("file_ext:"):
            die(f"source_registry.tsv line {i}: file row needs match_rule file_ext:…")
        if im == "text" and mr not in ("inline",) and not mr.startswith("text:"):
            die(f"source_registry.tsv line {i}: text row needs match_rule inline or text:…")
        if im == "url":
            if mr == "default":
                default_rows += 1
            elif not mr.startswith("host:"):
                die(f"source_registry.tsv line {i}: url row needs match_rule host:… or default")

        rd = row["raw_dir"]
        if not rd.startswith("raw/"):
            die(f"source_registry.tsv line {i}: raw_dir must start with raw/: {rd!r}")

        an, dn, dt = row["adapter_name"], row["dependency_name"], row["dependency_type"]
        if dt not in DEP_TYPES:
            die(f"source_registry.tsv line {i}: unknown dependency_type {dt!r}")

        if cat == "optional":
            if an == PLACEHOLDER or dn == PLACEHOLDER or dt == "none":
                die(f"source_registry.tsv line {i}: optional row must set adapter + dependency + non-none type")
        else:
            if an != PLACEHOLDER or dn != PLACEHOLDER or dt != "none":
                die(
                    f"source_registry.tsv line {i}: core/manual row must use "
                    f"{PLACEHOLDER}/{PLACEHOLDER}/none for adapter columns"
                )

    if default_rows != 1:
        die(f"expected exactly one url/default row (web catch-all), got {default_rows}")

    for need in CATEGORIES:
        if need not in cats:
            die(f"source_registry.tsv: missing at least one source_category={need!r}")


def extract_url_host(url: str) -> str:
    u = url.strip()
    if "://" not in u and "/" not in u.split("://", 1)[0]:
        u = "https://" + u
    parsed = urlparse(u)
    host = parsed.hostname or ""
    return host.lower()


def host_matches(host: str, pattern: str) -> bool:
    host = host.lower()
    pattern = pattern.strip().lower()
    return host == pattern or host.endswith("." + pattern)


def match_url(url: str, rows: list[dict[str, str]]) -> dict[str, str] | None:
    host = extract_url_host(url)
    if not host:
        return None
    fallback: dict[str, str] | None = None
    for row in rows:
        if row["input_mode"] != "url":
            continue
        mr = row["match_rule"]
        if mr == "default":
            fallback = row
            continue
        rest = mr[len("host:") :]
        for part in rest.split(","):
            pat = part.strip()
            if pat and host_matches(host, pat):
                return row
    return fallback


def match_file(path: str, rows: list[dict[str, str]]) -> dict[str, str] | None:
    lowered = path.lower()
    for row in rows:
        if row["input_mode"] != "file":
            continue
        exts = row["match_rule"][len("file_ext:") :].split(",")
        for ext in exts:
            e = ext.strip().lower()
            if e and lowered.endswith(e):
                return row
    return None


def row_tsv(row: dict[str, str]) -> str:
    return "\t".join(row[h] for h in EXPECTED_HEADER)


def cmd_validate(root: Path | None) -> int:
    tsv = registry_path()
    rows = load_rows(tsv)
    validate_rows(rows)
    wiki_root = root or tools_dir().parent
    try:
        disp = tsv.relative_to(wiki_root.resolve())
    except ValueError:
        disp = tsv
    print(f"ok: {len(rows)} sources, registry {disp}")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(description="source_registry.tsv CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("validate", help="validate TSV schema and consistency")
    pv.add_argument("wiki_root", nargs="?", help="only for display path; default parent of tools/")

    pm = sub.add_parser("match-url", help="print matching registry row (TSV line) for a URL")
    pm.add_argument("url")

    pf = sub.add_parser("match-file", help="print matching registry row for a local file path")
    pf.add_argument("path")

    pl = sub.add_parser("list", help="print all rows (TSV)")
    pl.add_argument("--category", choices=sorted(CATEGORIES))

    pg = sub.add_parser("get", help="print one row by source_id")
    pg.add_argument("source_id")

    pd = sub.add_parser("deps", help="unique dependency_name for dependency_type")
    pd.add_argument("dependency_type", choices=sorted(DEP_TYPES))

    plout = sub.add_parser(
        "layout",
        help="check minimal layout + taxonomy.md top shelves vs raw/<shelf>, wiki/<shelf>",
    )
    plout.add_argument("wiki_root")

    args = p.parse_args(argv)

    if args.cmd == "layout":
        root = Path(args.wiki_root).expanduser().resolve()
        required = [
            root / "CLAUDE.md",
            root / "taxonomy.md",
            root / "wiki",
            root / "raw",
            root / "tools" / "source_registry.tsv",
        ]
        missing = [p for p in required if not p.exists()]
        if missing:
            print("layout: missing:", file=sys.stderr)
            for p in missing:
                print(f"  {p}", file=sys.stderr)
            return 1
        tax = root / "taxonomy.md"
        shelves = taxonomy_top_shelves(tax)
        disk_err: list[str] = []
        for s in shelves:
            if not (root / "raw" / s).is_dir():
                disk_err.append(f"missing raw/{s}/ (listed in taxonomy.md)")
            if not (root / "wiki" / s).is_dir():
                disk_err.append(f"missing wiki/{s}/ (listed in taxonomy.md)")
        if disk_err:
            print("layout: taxonomy vs disk:", file=sys.stderr)
            for msg in disk_err:
                print(f"  {msg}", file=sys.stderr)
            return 1
        print(f"layout: ok {root}")
        return 0

    tsv = registry_path()
    rows = load_rows(tsv)
    validate_rows(rows)

    if args.cmd == "validate":
        root = Path(args.wiki_root).expanduser().resolve() if args.wiki_root else None
        return cmd_validate(root)

    if args.cmd == "match-url":
        m = match_url(args.url, rows)
        if not m:
            die(f"no match for url: {args.url!r}", 2)
        print(row_tsv(m))
        return 0

    if args.cmd == "match-file":
        m = match_file(args.path, rows)
        if not m:
            die(f"no match for path: {args.path!r}", 2)
        print(row_tsv(m))
        return 0

    if args.cmd == "list":
        for row in rows:
            if args.category and row["source_category"] != args.category:
                continue
            print(row_tsv(row))
        return 0

    if args.cmd == "get":
        for row in rows:
            if row["source_id"] == args.source_id:
                print(row_tsv(row))
                return 0
        die(f"unknown source_id: {args.source_id!r}", 2)

    if args.cmd == "deps":
        seen: set[str] = set()
        for row in rows:
            if row["dependency_type"] == args.dependency_type and row["dependency_name"] != PLACEHOLDER:
                seen.add(row["dependency_name"])
        for name in sorted(seen):
            print(name)
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
