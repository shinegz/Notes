#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Deterministic wiki lint: broken wikilinks, orphans (optional), source_file paths,
source frontmatter, optional strict ingest placeholders.

Usage:
  python3 lint_wiki.py <wiki-root>
  python3 lint_wiki.py --strict-ingest <wiki-root> # fail if Key claims still 占位

Ideas partly aligned with llm-wiki-agent/tools/lint.py (link/orphan checks only;
no API-based semantic lint).

Typed pages (YAML `type:` in first lines): require last_updated; reject deprecated `date:`.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

SKIP_NAMES = {"log.md", "lint-report.md"}
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def norm_target(raw: str) -> str:
    t = raw.strip()
    if "|" in t:
        t = t.split("|", 1)[0].strip()
    if "#" in t:
        t = t.split("#", 1)[0].strip()
    return t


def page_id(rel: Path) -> str:
    return rel.with_suffix("").as_posix()


def all_pages(wiki_dir: Path) -> list[Path]:
    return [p for p in wiki_dir.rglob("*.md") if p.is_file() and p.name not in SKIP_NAMES]


def build_indexes(pages: list[Path], wiki_dir: Path) -> tuple[dict[str, str], dict[str, list[str]]]:
    """Map normalized target -> canonical id; stem -> list of ids (detect ambiguity)."""
    id_set: set[str] = set()
    stem_to: dict[str, list[str]] = defaultdict(list)
    for p in pages:
        rel = p.relative_to(wiki_dir)
        pid = page_id(rel)
        id_set.add(pid)
        stem_to[p.stem.lower()].append(pid)
    return {i.lower(): i for i in id_set}, dict(stem_to)


def resolve_link(target: str, id_lower: dict[str, str], stem_to: dict[str, list[str]]) -> str | None:
    t = norm_target(target)
    if not t:
        return None
    tl = t.lower()
    if tl in id_lower:
        return id_lower[tl]
    if t in id_lower:
        return id_lower[t]
    if tl in stem_to and len(stem_to[tl]) == 1:
        return stem_to[tl][0]
    if "/" in t:
        suf = t.split("/")[-1].lower()
        if suf in stem_to and len(stem_to[suf]) == 1:
            return stem_to[suf][0]
    return None


def extract_links(text: str) -> list[str]:
    return [norm_target(m.group(1)) for m in WIKILINK_RE.finditer(text)]


def frontmatter_field(text: str, key: str) -> str | None:
    prefix = f"{key}:"
    for line in text.splitlines()[:80]:
        s = line.strip()
        if s.startswith(prefix):
            return s[len(prefix) :].strip().strip('"').strip("'")
    return None


def is_source_page(text: str) -> bool:
    t = frontmatter_field(text, "type")
    return (t or "").lower() == "source"


def key_claims_section_has_placeholder(text: str) -> bool:
    """True if ## Key claims section exists and still contains ingest 占位."""
    lines = text.splitlines()
    in_claims = False
    for line in lines:
        if line.strip().lower().startswith("## key claims"):
            in_claims = True
            continue
        if in_claims:
            if line.startswith("## ") and "key claims" not in line.lower():
                break
            if "ingest 占位" in line or "ingest占位" in line:
                return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Deterministic wiki lint")
    ap.add_argument("wiki_root", type=Path, help="llm-wiki root (contains wiki/)")
    ap.add_argument(
        "--strict-ingest",
        action="store_true",
        help="fail if type: source pages still have 占位 in Key claims",
    )
    args = ap.parse_args()
    root = args.wiki_root.expanduser().resolve()
    wiki_dir = root / "wiki"
    if not wiki_dir.is_dir():
        print("missing wiki/", file=sys.stderr)
        return 1

    pages = all_pages(wiki_dir)
    id_lower, stem_to = build_indexes(pages, wiki_dir)
    id_set = set(id_lower.values())

    broken: list[tuple[str, str, str]] = []
    inbound: dict[str, int] = defaultdict(int)

    for p in pages:
        text = p.read_text(encoding="utf-8", errors="ignore")
        src_id = page_id(p.relative_to(wiki_dir))
        for raw in extract_links(text):
            if not raw or raw.startswith("http"):
                continue
            tgt = resolve_link(raw, id_lower, stem_to)
            if tgt is None or tgt not in id_set:
                broken.append((src_id, raw, "unresolved"))
            else:
                inbound[tgt] += 1

    orphans = [page_id(p.relative_to(wiki_dir)) for p in pages if inbound.get(page_id(p.relative_to(wiki_dir)), 0) == 0]
    orphans = [o for o in orphans if o not in ("overview", "index") and not o.endswith("/overview")]

    missing_raw: list[tuple[str, str]] = []
    frontmatter_errors: list[tuple[str, str]] = []
    source_url_warnings: list[str] = []
    thin_ingest: list[str] = []
    for p in pages:
        text = p.read_text(encoding="utf-8", errors="ignore")
        pid = page_id(p.relative_to(wiki_dir))
        page_type = (frontmatter_field(text, "type") or "").strip()
        if page_type:
            if not (frontmatter_field(text, "last_updated") or "").strip():
                frontmatter_errors.append((pid, "missing last_updated"))
            if (frontmatter_field(text, "date") or "").strip():
                frontmatter_errors.append((pid, "deprecated frontmatter key date: use last_updated"))
        if not is_source_page(text):
            continue
        title = (frontmatter_field(text, "title") or "").strip()
        sf = (frontmatter_field(text, "source_file") or "").strip()
        su = (frontmatter_field(text, "source_url") or "").strip()
        if not title:
            frontmatter_errors.append((pid, "missing title"))
        if not sf:
            frontmatter_errors.append((pid, "missing source_file"))
        if not su:
            source_url_warnings.append(pid)
        if sf and not sf.startswith("http"):
            candidate = (root / sf).resolve()
            try:
                candidate.relative_to(root.resolve())
            except ValueError:
                missing_raw.append((pid, f"{sf} (outside wiki root)"))
            else:
                if not candidate.is_file():
                    missing_raw.append((pid, sf))
        if key_claims_section_has_placeholder(text):
            thin_ingest.append(pid)

    print(f"pages: {len(pages)}")
    print(f"broken_links: {len(broken)}")
    for src, link, _ in broken[:40]:
        print(f"  {src} -> [[{link}]]")
    if len(broken) > 40:
        print(f"  ... ({len(broken) - 40} more)")
    print(f"orphan_pages (heuristic): {len(orphans)}")
    for o in orphans[:20]:
        print(f"  {o}")
    if len(orphans) > 20:
        print(f"  ... ({len(orphans) - 20} more)")
    print(f"missing_source_file: {len(missing_raw)}")
    for sid, sf in missing_raw[:40]:
        print(f"  {sid} -> source_file {sf!r}")
    if len(missing_raw) > 40:
        print(f"  ... ({len(missing_raw) - 40} more)")
    print(f"source_frontmatter_errors: {len(frontmatter_errors)}")
    for pid, reason in frontmatter_errors[:30]:
        print(f"  {pid} -> {reason}")
    if len(frontmatter_errors) > 30:
        print(f"  ... ({len(frontmatter_errors) - 30} more)")
    if source_url_warnings:
        print(f"source_url_missing (warning): {len(source_url_warnings)}")
        for pid in source_url_warnings[:20]:
            print(f"  {pid}")
        if len(source_url_warnings) > 20:
            print(f"  ... ({len(source_url_warnings) - 20} more)")
    print(f"thin_key_claims (ingest 占位): {len(thin_ingest)}")
    for t in thin_ingest[:20]:
        print(f"  {t}")
    if len(thin_ingest) > 20:
        print(f"  ... ({len(thin_ingest) - 20} more)")

    fail = bool(broken or missing_raw or frontmatter_errors)
    if args.strict_ingest and thin_ingest:
        fail = True
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
