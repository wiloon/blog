#!/usr/bin/env python3
"""
fix_tags.py — 批量规范化博客文章的 tags 字段

用法:
    # 预览变更（不写入文件）
    python3 tools/fix_tags.py --dry-run

    # 实际写入
    python3 tools/fix_tags.py

    # 查看统计信息
    python3 tools/fix_tags.py --dry-run --stats
"""

import os
import re
import sys
import argparse
from pathlib import Path

# ─────────────────────────────────────────────
# 映射规则：旧值（小写，去引号） → 新值
# 注意：匹配时先去掉首尾引号，再转小写
# ─────────────────────────────────────────────
TAG_MAP: dict[str, str] = {
    # ── 特殊内容类标签（统一小写，保持现有约定） ─────────
    "inbox":        "Inbox",
    "reprint":      "reprint",
    "remix":        "remix",
    "ai-assisted":  "AI-assisted",
    "original":     "original",

    # ── 编程语言 ──────────────────────────────
    "java":         "Java",
    "go":           "Go",
    "golang":       "Go",
    "python":       "Python",
    "javascript":   "JavaScript",
    "js":           "JavaScript",
    "typescript":   "TypeScript",
    "ts":           "TypeScript",
    "rust":         "Rust",
    "kotlin":       "Kotlin",
    "scala":        "Scala",
    "groovy":       "Groovy",
    "lua":          "Lua",
    "dart":         "Dart",
    "c":            "C",
    "c++":          "C++",
    "dotnet":       "dotnet",
    "bat":          "bat",

    # ── 操作系统 / 发行版 ─────────────────────
    "linux":        "Linux",
    "arch linux":   "Linux",
    "archlinux":    "Linux",
    "ubuntu":       "Ubuntu",
    "redhat":       "RedHat",
    "fedora":       "Fedora",
    "windows":      "Windows",
    "macos":        "macOS",
    "mac os":       "macOS",

    # ── 数据库 ────────────────────────────────
    "mysql":        "MySQL",
    "redis":        "Redis",
    "postgresql":   "PostgreSQL",
    "sqlite":       "SQLite",
    "mongodb":      "MongoDB",
    "h2":           "H2",
    "derby":        "Derby",
    "hbase":        "HBase",
    "influxdb":     "InfluxDB",
    "memcache":     "Memcache",
    "memcached":    "Memcache",
    "nosql":        "NoSQL",

    # ── 框架 / 库 ─────────────────────────────
    "spring":       "Spring",
    "maven":        "Maven",
    "gradle":       "Gradle",
    "netty":        "Netty",
    "tomcat":       "Tomcat",
    "jpa":          "JPA",
    "servlet":      "Servlet",
    "mybatis":      "MyBatis",
    "junit":        "JUnit",
    "kafka":        "Kafka",
    "ansible":      "Ansible",
    "babel":        "Babel",
    "axios":        "axios",
    "langchain":    "LangChain",
    "crewai":       "CrewAI",
    "nutch":        "Nutch",
    "nexus":        "Nexus",

    # ── 工具 ──────────────────────────────────
    "git":          "Git",
    "vim":          "VIM",
    "emacs":        "Emacs",
    "docker":       "Docker",
    "npm":          "npm",
    "node":         "Node.js",
    "openwrt":      "OpenWrt",
    "kaniko":       "kaniko",

    # ── 协议 / 概念 ───────────────────────────
    "network":      "Network",
    "tcp":          "TCP",
    "vpn":          "VPN",
    "nat":          "NAT",
    "ssh":          "SSH",
    "http":         "HTTP",
    "html":         "HTML",
    "css":          "CSS",
    "xml":          "XML",
    "xml":          "XML",
    "json":         "JSON",
    "regex":        "Regex",
    "ftp":          "FTP",

    # ── 硬件 / 平台 ───────────────────────────
    "raspberry pi": "Raspberry Pi",
    "kvm":          "KVM",
    "gpu":          "GPU",

    # ── 方法论 / 工程 ─────────────────────────
    "scrum":        "Agile",        # 合并到 Agile
    "agile":        "Agile",
    "designpattern": "Pattern",     # 合并到 Pattern
    "design-pattern": "Pattern",
    "pattern":      "Pattern",
    "security":     "Security",
    "concurrent":   "concurrent",
    "thread":       "thread",
    "lock":         "lock",
    "io":           "IO",
    "gc":           "GC",
    "queue":        "Queue",
    "coroutine":    "Coroutine",
    "exception":    "Exception",
    "collection":   "Collection",
    "map":          "Map",
    "ipc":          "IPC",

    # ── 其他规范写法 ─────────────────────────
    "shell":        "Shell",
    "command":      "Command",
    "web":          "Web",
    "ai":           "AI",
    "math":         "Math",
    "english":      "English",
    "algorithm":    "Algorithm",
    "cloud":        "Cloud",
    "database":     "Database",
    "data structure": "Algorithm",
    "cs":           "CS",
    "hardware":     "Hardware",
    "tools":        "Tools",
    "desktop":      "Desktop",
    "javascript":   "JavaScript",
    "life":         "Life",
    "music":        "Music",
    "font":         "Font",
    "chrome":       "chrome",
    "idea":         "IDEA",
    "kde":          "KDE",
    "jboss":        "JBoss",
    "excel":        "Excel",
    "libreoffice":  "LibreOffice",
    "etl":          "ETL",
    "lvm":          "LVM",
    "mq":           "MQ",
    "k8s":          "k8s",
    "ci/cd":        "CI/CD",
    "homelab":      "HomeLab",
    "proxy":        "proxy",
    "monitoring":   "monitoring",
    "monitor":      "monitoring",
    "memory":       "memory",
    "mmap":         "mmap",
    "kernel":       "kernel",
    "disk":         "disk",
    "file":         "file",
    "mail":         "Mail",
    "maths":        "Math",
    "hack":         "Hack",
    "language":     "Language",
    "grammar":      "Grammar",
    "cooking":      "Cooking",
    "car":          "Car",
    "logistics":    "Logistics",
    "kindergarten": "Kindergarten",
    "github":       "GitHub",
    "aws":          "AWS",
    "find":         "find",
    "codepage":     "codepage",
    "java":         "Java",
    "interactive rebase": "Git",
}

CONTENT_DIR = Path(__file__).parent.parent / "content" / "post"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
TAGS_BLOCK_RE = re.compile(
    r"(^tags:\s*\n)((?:[ \t]+-[ \t]+.+\n?)*)", re.MULTILINE
)


def strip_quotes(val: str) -> str:
    """去掉首尾的单引号或双引号。"""
    for q in ('"', "'"):
        if val.startswith(q) and val.endswith(q) and len(val) >= 2:
            return val[1:-1]
    return val


def normalize_tag(tag: str) -> str | None:
    """
    返回规范化后的 tag 值。
    None 表示不需要修改（已经是正确值）。
    """
    stripped = strip_quotes(tag.strip())
    mapped = TAG_MAP.get(stripped.lower())
    if mapped is None:
        # 只去引号，不做其他修改
        if stripped != tag.strip():
            return stripped
        return None
    if mapped == stripped:
        return None   # 已经正确
    return mapped


def process_file(path: Path, dry_run: bool) -> tuple[bool, list[tuple[str, str]]]:
    text = path.read_text(encoding="utf-8")
    fm_match = FRONT_MATTER_RE.match(text)
    if not fm_match:
        return False, []

    fm_body = fm_match.group(1)
    tag_block = TAGS_BLOCK_RE.search(fm_body)
    if not tag_block:
        return False, []

    header = tag_block.group(1)
    items_str = tag_block.group(2)

    item_re = re.compile(r"([ \t]+-[ \t]+)(.+)")
    changes: list[tuple[str, str]] = []
    new_lines: list[str] = []
    modified = False

    for line in items_str.splitlines(keepends=True):
        m = item_re.match(line.rstrip("\n"))
        if m:
            indent_dash = m.group(1)
            old_val = m.group(2).strip()
            new_val = normalize_tag(old_val)
            ending = "\n" if line.endswith("\n") else ""
            if new_val is not None and new_val != old_val:
                changes.append((old_val, new_val))
                new_lines.append(f"{indent_dash}{new_val}{ending}")
                modified = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if not modified:
        return False, []

    if dry_run:
        return True, changes

    new_items_str = "".join(new_lines)
    new_fm_body = (
        fm_body[: tag_block.start()]
        + header
        + new_items_str
        + fm_body[tag_block.end():]
    )
    new_text = text[: fm_match.start(1)] + new_fm_body + text[fm_match.end(1):]
    path.write_text(new_text, encoding="utf-8")
    return True, changes


def main() -> None:
    parser = argparse.ArgumentParser(description="规范化博客文章 tags 字段")
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

    mode = "[DRY RUN] " if args.dry_run else "[APPLIED] "
    for filepath, changes in all_changes.items():
        for old_val, new_val in changes:
            print(f"{mode}{filepath}: '{old_val}' → '{new_val}'")

    print(f"\n{'Preview' if args.dry_run else 'Modified'}: {total_modified} file(s)")

    if args.stats:
        from collections import Counter
        counter: Counter[str] = Counter()
        for changes in all_changes.values():
            for old_val, new_val in changes:
                counter[f"'{old_val}' → '{new_val}'"] += 1
        print("\nTop changes:")
        for change, count in counter.most_common(30):
            print(f"  {count:4d}x  {change}")

    if args.dry_run and total_modified > 0:
        print("\nRun without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
