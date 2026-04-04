#!/usr/bin/env python3
"""
fix_categories.py — 批量规范化博客文章的 categories 字段

用法:
    # 预览变更（不写入文件）
    python3 tools/fix_categories.py --dry-run

    # 实际写入
    python3 tools/fix_categories.py

    # 查看统计信息
    python3 tools/fix_categories.py --dry-run --stats
"""

import os
import re
import sys
import argparse
from pathlib import Path

# ─────────────────────────────────────────────
# 映射规则：旧值 → 新值（键全部小写，用于不区分大小写匹配）
# ─────────────────────────────────────────────
CATEGORY_MAP: dict[str, str] = {
    # Go
    "golang": "Go",

    # Python
    "python": "Python",

    # JavaScript
    "javascript": "JavaScript",
    "js": "JavaScript",

    # Java（合并 Spring、Maven 到 Java 等）
    "spring": "Java",
    "maven": "Java",

    # Linux（合并 shell、command 类）
    "linux": "Linux",
    "shell": "Linux",
    "command": "Linux",
    "commands": "Linux",
    "os": "Linux",
    "filesystem": "Linux",
    "system": "Linux",

    # Network
    "network": "Network",
    "http": "Network",
    "ssh": "Network",
    "socks5": "Network",
    "router": "Network",
    "w10n": "Network",

    # Database（合并 db、redis、mysql 等）
    "database": "Database",
    "databases": "Database",
    "db": "Database",
    "redis": "Database",
    "mysql": "Database",
    "cache": "Database",
    "mq": "Database",
    "ipc": "Database",

    # Cloud（合并 container、k8s、CI、devops）
    "cloud": "Cloud",
    "container": "Cloud",
    "k8s": "Cloud",
    "ci": "Cloud",
    "devops": "Cloud",

    # Web（合并 nginx、restful）
    "web": "Web",
    "nginx": "Web",
    "restful": "Web",

    # Algorithm（合并 Data-Structure 变体）
    "algorithm": "Algorithm",
    "data-structure": "Algorithm",
    "datastructure": "Algorithm",
    "data structure": "Algorithm",

    # Pattern（合并 Architecture、DDD、UML）
    "pattern": "Pattern",
    "architecture": "Pattern",
    "ddd": "Pattern",
    "uml": "Pattern",

    # Hardware（合并 Raspberry-Pi、GPU）
    "hardware": "Hardware",
    "raspberry-pi": "Hardware",
    "raspberry pi": "Hardware",
    "gpu": "Hardware",
    "electronic": "Hardware",

    # Desktop（合并 Windows、macOS、VM）
    "desktop": "Desktop",
    "windows": "Desktop",
    "macos": "Desktop",
    "vm": "Desktop",

    # Tools（合并 Editor、Emacs、VIM、Git、VCS、Eclipse、IDE）
    "editor": "Tools",
    "emacs": "Tools",
    "vim": "Tools",
    "ide": "Tools",
    "git": "Tools",
    "vcs": "Tools",
    "eclipse": "Tools",

    # AI
    "ai": "AI",

    # Math
    "math": "Math",

    # English
    "english": "English",

    # Agile（合并 Scrum）
    "agile": "Agile",
    "scrum": "Agile",

    # CS（合并 cs、Computer Science、development、dev）
    "cs": "CS",
    "computer science": "CS",
    "development": "CS",
    "dev": "CS",
    "text": "CS",

    # Life（合并 Law、Science、Photography、Music、Book、artwork）
    "law": "Life",
    "science": "Life",
    "photography": "Life",
    "music": "Life",
    "book": "Life",
    "artwork": "Life",

    # Security
    "security": "Security",

    # 其他保持规范大小写
    "reprint": "reprint",  # 应该是 tag，不动（单独处理）
    "java": "Java",
    "go": "Go",
    "network": "Network",
    "web": "Web",
    "linux": "Linux",
    "database": "Database",
    "cloud": "Cloud",
    "hardware": "Hardware",
    "desktop": "Desktop",
    "tools": "Tools",
    "math": "Math",
    "english": "English",
    "agile": "Agile",
    "algorithm": "Algorithm",
    "pattern": "Pattern",
    "security": "Security",
    "life": "Life",
    "kafka": "Database",
    "netty": "Java",
    "lock": "CS",
    "log": "CS",
}

# 保留不动的分类（值完全匹配，不做任何修改）
KEEP_AS_IS: set[str] = {
    "Inbox",
    "inbox",
    "Chinese",
    "chrome",
}

CONTENT_DIR = Path(__file__).parent.parent / "content" / "post"


def normalize_category(cat: str) -> str | None:
    """返回规范化后的分类名，None 表示不需要修改。"""
    stripped = cat.strip()
    if stripped in KEEP_AS_IS:
        return None
    lower = stripped.lower()
    mapped = CATEGORY_MAP.get(lower)
    if mapped is None:
        return None  # 不在映射表中，保持原样
    if mapped == stripped:
        return None  # 已经是正确值，无需修改
    return mapped


FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
CATEGORIES_BLOCK_RE = re.compile(
    r"(^categories:\s*\n)((?:[ \t]+-[ \t]+.+\n?)*)", re.MULTILINE
)


def process_file(path: Path, dry_run: bool) -> tuple[bool, list[tuple[str, str]]]:
    """
    处理单个文件。
    返回 (modified: bool, changes: list[(old_cat, new_cat)])
    """
    text = path.read_text(encoding="utf-8")

    fm_match = FRONT_MATTER_RE.match(text)
    if not fm_match:
        return False, []

    fm_body = fm_match.group(1)
    cat_block_match = CATEGORIES_BLOCK_RE.search(fm_body)
    if not cat_block_match:
        return False, []

    header = cat_block_match.group(1)   # "categories:\n"
    items_str = cat_block_match.group(2)  # "  - Foo\n  - Bar\n"

    item_re = re.compile(r"([ \t]+-[ \t]+)(.+)")
    changes: list[tuple[str, str]] = []
    new_items_lines: list[str] = []
    modified = False

    for line in items_str.splitlines(keepends=True):
        m = item_re.match(line.rstrip("\n"))
        if m:
            indent_dash = m.group(1)
            old_val = m.group(2).strip()
            new_val = normalize_category(old_val)
            ending = "\n" if line.endswith("\n") else ""
            if new_val is not None and new_val != old_val:
                changes.append((old_val, new_val))
                new_items_lines.append(f"{indent_dash}{new_val}{ending}")
                modified = True
            else:
                new_items_lines.append(line)
        else:
            new_items_lines.append(line)

    if not modified:
        return False, []

    if dry_run:
        return True, changes

    new_items_str = "".join(new_items_lines)
    new_fm_body = fm_body[: cat_block_match.start()] + header + new_items_str + fm_body[cat_block_match.end():]
    new_text = text[: fm_match.start(1)] + new_fm_body + text[fm_match.end(1):]
    path.write_text(new_text, encoding="utf-8")
    return True, changes


def main() -> None:
    parser = argparse.ArgumentParser(description="规范化博客文章 categories 字段")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不写入文件")
    parser.add_argument("--stats", action="store_true", help="额外显示统计摘要")
    args = parser.parse_args()

    md_files = sorted(CONTENT_DIR.rglob("*.md"))
    total_modified = 0
    all_changes: dict[str, list[tuple[str, str]]] = {}

    for f in md_files:
        modified, changes = process_file(f, dry_run=args.dry_run)
        if modified:
            total_modified += 1
            rel = str(f.relative_to(CONTENT_DIR.parent.parent))
            all_changes[rel] = changes

    # ── 输出报告 ──────────────────────────────
    mode = "[DRY RUN] " if args.dry_run else "[APPLIED] "
    for filepath, changes in all_changes.items():
        for old_val, new_val in changes:
            print(f"{mode}{filepath}: '{old_val}' → '{new_val}'")

    print(f"\n{'Preview' if args.dry_run else 'Modified'}: {total_modified} file(s)")

    if args.stats:
        from collections import Counter
        counter: Counter[str] = Counter()
        for changes in all_changes.values():
            for _, new_val in changes:
                counter[new_val] += 1
        print("\nCategory change frequency:")
        for cat, count in counter.most_common():
            print(f"  {cat}: {count}")

    if args.dry_run and total_modified > 0:
        print("\nRun without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
