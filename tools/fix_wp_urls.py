#!/usr/bin/env python3
"""
fix_wp_urls.py — 批量将 WordPress 遗留 URL（/?p=xxxx）替换为基于文件名的语义化 URL

用法:
    # 预览变更（不写入文件）
    python3 tools/fix_wp_urls.py --dry-run

    # 实际写入
    python3 tools/fix_wp_urls.py

    # 只预览前 N 条
    python3 tools/fix_wp_urls.py --dry-run --limit 20
"""

import re
import sys
import argparse
from pathlib import Path

CONTENT_DIR = Path(__file__).parent.parent / "content" / "post"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
# 匹配 url: /?p=数字 （有无引号、有无尾部斜线均支持）
WP_URL_RE = re.compile(r"""^(url:\s*)['"]?\/\?p=\d+\/?['"]?\s*$""", re.MULTILINE)


def slug_from_path(path: Path) -> str:
    """
    用文件名（不含扩展名）生成 URL slug。
    已经是英文 kebab-case 的直接使用；中文文件名也直接使用（Hugo 会自动处理编码）。
    """
    return path.stem


def process_file(path: Path, dry_run: bool) -> tuple[bool, str, str]:
    """
    返回 (是否修改, 旧 url 值, 新 url 值)
    """
    text = path.read_text(encoding="utf-8")
    fm_match = FRONT_MATTER_RE.match(text)
    if not fm_match:
        return False, "", ""

    fm_body = fm_match.group(1)
    m = WP_URL_RE.search(fm_body)
    if not m:
        return False, "", ""

    old_line = m.group(0).strip()
    new_slug = slug_from_path(path)
    new_line = f"url: {new_slug}"

    if dry_run:
        return True, old_line, new_line

    new_fm_body = WP_URL_RE.sub(f"url: {new_slug}", fm_body, count=1)
    new_text = text[: fm_match.start(1)] + new_fm_body + text[fm_match.end(1):]
    path.write_text(new_text, encoding="utf-8")
    return True, old_line, new_line


def main() -> None:
    parser = argparse.ArgumentParser(description="将 WordPress 旧 URL 替换为语义化文件名 URL")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不写入文件")
    parser.add_argument("--limit", type=int, default=0, help="只处理前 N 个文件（0=不限制）")
    args = parser.parse_args()

    md_files = sorted(CONTENT_DIR.rglob("*.md"))
    total_modified = 0
    count = 0

    for f in md_files:
        if args.limit and count >= args.limit:
            break
        modified, old_url, new_url = process_file(f, dry_run=args.dry_run)
        if modified:
            total_modified += 1
            count += 1
            rel = str(f.relative_to(CONTENT_DIR.parent.parent))
            mode = "[DRY RUN]" if args.dry_run else "[APPLIED]"
            print(f"{mode} {rel}")
            print(f"         {old_url}")
            print(f"      -> {new_url}")

    action = "Preview" if args.dry_run else "Modified"
    print(f"\n{action}: {total_modified} file(s)")


if __name__ == "__main__":
    main()
