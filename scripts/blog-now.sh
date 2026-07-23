#!/usr/bin/env bash
# Print current time in Asia/Shanghai (UTC+8) for blog front matter.
# Usage:
#   bash scripts/blog-now.sh          # 2026-07-23T16:36:57+08:00
#   bash scripts/blog-now.sh --date   # 2026-07-23  (for "is lastmod today?" checks)
set -euo pipefail

case "${1:-}" in
  --date|-d)
    TZ=Asia/Shanghai date '+%Y-%m-%d'
    ;;
  ""|--now|-n)
    TZ=Asia/Shanghai date '+%Y-%m-%dT%H:%M:%S+08:00'
    ;;
  -h|--help)
    cat <<'EOF'
Usage: bash scripts/blog-now.sh [--date|--now]

Print current Asia/Shanghai time for date/lastmod fields.
Always converts from the machine clock; never appends +08:00 to local digits.

  (default) / --now   full timestamp: YYYY-MM-DDTHH:MM:SS+08:00
  --date / -d         date only: YYYY-MM-DD
EOF
    ;;
  *)
    echo "unknown option: $1 (try --help)" >&2
    exit 1
    ;;
esac
