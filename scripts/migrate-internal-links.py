#!/usr/bin/env python3
"""Migrate Hugo /permalink Markdown links to relative .md paths."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"

LINK_RE = re.compile(r"\]\((/[^)#\s]+)(#[^)]+)?\)")

SKIP_EXACT = {"/url"}
SKIP_PREFIXES = ("/user/",)

JAVA_SCOPE_DIRS = (
    CONTENT_DIR / "post" / "language" / "java",
    CONTENT_DIR / "post" / "cs",
)

SDD_TAG_OVERRIDES: dict[str, list[str]] = {
    "content/post/language/java/java-knowledge-map.md": [
        "original",
        "AI-assisted",
        "java",
        "jvm",
    ],
}


@dataclass
class Report:
    replacements: dict[str, list[tuple[str, str]]] = field(default_factory=dict)
    skipped: list[tuple[str, int, str, str]] = field(default_factory=list)
    unresolved: list[tuple[str, int, str]] = field(default_factory=list)
    ambiguous: list[tuple[str, str, list[str]]] = field(default_factory=list)
    touched: list[str] = field(default_factory=list)

    @property
    def total_replacements(self) -> int:
        return sum(len(v) for v in self.replacements.values())


def parse_frontmatter(text: str) -> tuple[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not match:
        return "", text
    return match.group(1), text[match.end() :]


def is_draft(fm: str) -> bool:
    return bool(re.search(r"^draft:\s*true\s*$", fm, re.MULTILINE))


def rank_candidate(path: str) -> tuple:
    p = path.replace("\\", "/")
    return (
        "/inbox/" in p,
        is_draft(parse_frontmatter(Path(REPO_ROOT / path).read_text(encoding="utf-8"))[0])
        if Path(REPO_ROOT / path).exists()
        else False,
        -p.count("/"),
        p,
    )


def build_index(content_dir: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    url_index: dict[str, list[str]] = defaultdict(list)
    stem_index: dict[str, list[str]] = defaultdict(list)

    for md in content_dir.rglob("*.md"):
        rel = md.relative_to(REPO_ROOT).as_posix()
        text = md.read_text(encoding="utf-8", errors="replace")
        fm, _ = parse_frontmatter(text)
        stem_index[md.stem.lower()].append(rel)
        if fm:
            url_match = re.search(r"^url:\s*(.+)$", fm, re.MULTILINE)
            if url_match:
                url = url_match.group(1).strip().strip("'\"")
                if url:
                    url_index[url.lstrip("/")].append(rel)
    return url_index, stem_index


def pick_candidate(candidates: list[str]) -> tuple[str | None, list[str]]:
    if not candidates:
        return None, []
    unique = sorted(set(candidates), key=rank_candidate)
    if len(unique) > 1 and rank_candidate(unique[0]) == rank_candidate(unique[1]):
        return None, unique
    return unique[0], []


def resolve_target(
    permalink: str,
    url_index: dict[str, list[str]],
    stem_index: dict[str, list[str]],
) -> tuple[str | None, list[str]]:
    key = permalink.lstrip("/")
    if key in url_index:
        return pick_candidate(url_index[key])

    slug = key.split("/")[-1].lower()
    if slug in stem_index:
        return pick_candidate(stem_index[slug])

    return None, []


def should_skip(path: str) -> str | None:
    if path in SKIP_EXACT:
        return "skip-target"
    for prefix in SKIP_PREFIXES:
        if path.startswith(prefix):
            return "static-asset"
    if "." in Path(path).name and not path.endswith(".md"):
        return "static-asset"
    return None


def normalize_rel(from_dir: Path, target_rel: str) -> str:
    target = REPO_ROOT / target_rel
    result = Path(__import__("os").path.relpath(target, start=from_dir)).as_posix()
    if not result.startswith("."):
        result = "./" + result
    return result


def iter_body_lines(body: str):
    in_code = False
    for line_no, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            yield line_no, line, True
            continue
        yield line_no, line, in_code


def migrate_file(
    md_path: Path,
    url_index: dict[str, list[str]],
    stem_index: dict[str, list[str]],
    report: Report,
) -> str | None:
    text = md_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if not fm and text.startswith("---"):
        return None

    new_lines: list[str] = []
    file_key = md_path.relative_to(REPO_ROOT).as_posix()
    changed = False

    for line_no, line, in_code in iter_body_lines(body):
        if in_code:
            new_lines.append(line)
            continue

        def replacer(match: re.Match) -> str:
            nonlocal changed
            path = match.group(1)
            anchor = match.group(2) or ""
            skip_reason = should_skip(path)
            if skip_reason:
                report.skipped.append((file_key, line_no, path + anchor, skip_reason))
                return match.group(0)

            target, amb = resolve_target(path, url_index, stem_index)
            if amb:
                report.ambiguous.append((path, file_key, amb))
                return match.group(0)
            if not target:
                report.unresolved.append((file_key, line_no, path + anchor))
                return match.group(0)

            new_dest = normalize_rel(md_path.parent, target) + anchor
            old_dest = path + anchor
            if new_dest != old_dest:
                changed = True
                report.replacements.setdefault(file_key, []).append((old_dest, new_dest))
            return f"]({new_dest})"

        new_line = LINK_RE.sub(replacer, line)
        new_lines.append(new_line)

    if not changed:
        return None

    new_body = "\n".join(new_lines)
    if body.endswith("\n"):
        new_body += "\n"
    return f"---\n{fm.rstrip()}\n---\n{new_body}" if fm else new_body


def update_tags(fm: str, file_key: str) -> str:
    if file_key in SDD_TAG_OVERRIDES:
        desired = SDD_TAG_OVERRIDES[file_key]
    else:
        tags_block = re.search(r"^tags:\n((?:  - .+\n)*)", fm, re.MULTILINE)
        existing: list[str] = []
        if tags_block:
            existing = [
                m.group(1)
                for m in re.finditer(r"^  - (.+)$", tags_block.group(1), re.MULTILINE)
            ]
        tag_set = {t.strip() for t in existing}
        tag_set.discard("reprint")
        if "original" in tag_set:
            tag_set.discard("remix")
            tag_set.add("AI-assisted")
        else:
            tag_set.add("remix")
            tag_set.add("AI-assisted")
        desired = sorted(tag_set)

    fm = re.sub(r"^tags:\n(?:  - .+(?:\n|$))*", "", fm, count=1, flags=re.MULTILINE)
    fm = re.sub(r"^categories:\n((?:  - .+\n)*)  - AI-assisted\n", r"categories:\n\1", fm, count=1, flags=re.MULTILINE)
    fm = fm.rstrip("\n") + "\n"
    tags_yaml = "tags:\n" + "".join(f"  - {t}\n" for t in desired)
    return fm + tags_yaml


def apply_write(md_path: Path, new_content: str, report: Report) -> None:
    file_key = md_path.relative_to(REPO_ROOT).as_posix()
    fm, body = parse_frontmatter(new_content)
    if fm:
        fm = update_tags(fm, file_key)
        final = f"---\n{fm.rstrip()}\n---\n{body}"
    else:
        final = new_content
    md_path.write_text(final, encoding="utf-8")
    report.touched.append(file_key)


def collect_files(scope: str, file_arg: str | None) -> list[Path]:
    if file_arg:
        path = Path(file_arg)
        if not path.is_absolute():
            path = REPO_ROOT / path
        if not path.exists() or path.suffix != ".md":
            print(f"ERROR: --file must point to an existing .md: {file_arg}", file=sys.stderr)
            sys.exit(1)
        return [path]

    if scope == "java":
        files: list[Path] = []
        for d in JAVA_SCOPE_DIRS:
            if d.exists():
                files.extend(d.rglob("*.md"))
        return sorted(set(files))

    return sorted(CONTENT_DIR.rglob("*.md"))


def print_report(report: Report) -> None:
    print(f"=== Summary ===")
    print(f"Files with replacements: {len(report.replacements)}")
    print(f"Total replacements: {report.total_replacements}")
    print(f"Skipped: {len(report.skipped)}")
    print(f"Unresolved: {len(report.unresolved)}")
    print(f"Ambiguous: {len(report.ambiguous)}")
    print()

    for file_key, pairs in sorted(report.replacements.items()):
        print(f"--- {file_key} ({len(pairs)} links) ---")
        for old, new in pairs[:5]:
            print(f"  {old}  ->  {new}")
        if len(pairs) > 5:
            print(f"  ... and {len(pairs) - 5} more")

    if report.skipped:
        print("\n=== SKIPPED ===")
        for file_key, line_no, dest, reason in report.skipped:
            print(f"  {file_key}:{line_no}  {dest}  ({reason})")

    if report.unresolved:
        print("\n=== UNRESOLVED ===")
        for file_key, line_no, dest in report.unresolved:
            print(f"  {file_key}:{line_no}  {dest}")

    if report.ambiguous:
        print("\n=== AMBIGUOUS ===")
        for path, file_key, cands in report.ambiguous:
            print(f"  {path} in {file_key}: {cands}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate /permalink links to relative .md paths")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Report only, do not write")
    mode.add_argument("--write", action="store_true", help="Apply changes in place")
    parser.add_argument("--scope", choices=("all", "java"), default="all")
    parser.add_argument("--file", help="Process a single markdown file only")
    args = parser.parse_args()

    files = collect_files(args.scope if not args.file else "all", args.file)
    url_index, stem_index = build_index(CONTENT_DIR)
    report = Report()

    pending: dict[Path, str] = {}
    for md in files:
        new_content = migrate_file(md, url_index, stem_index, report)
        if new_content is not None:
            pending[md] = new_content

    print_report(report)

    if report.unresolved or report.ambiguous:
        print("\nERROR: unresolved or ambiguous links; no files written.", file=sys.stderr)
        return 1

    if args.write:
        for md, content in pending.items():
            apply_write(md, content, report)
        print(f"\nWrote {len(pending)} file(s).")
    elif pending:
        print(f"\nDry run: would write {len(pending)} file(s). Use --write to apply.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
