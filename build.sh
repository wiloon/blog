#!/bin/bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

count=$(find content/post -name "*.md" | wc -l | tr -d ' ')
chars=$(find content/post -name "*.md" -exec cat {} + | wc -m | tr -d ' ')
ts=$(date +%s)
mkdir -p static
echo "{\"article_count\":${count},\"total_chars\":${chars},\"generated_at\":${ts}}" \
  > static/stats.json
echo "article_count=${count}, total_chars=${chars}"

exec "${ROOT}/scripts/build-site.sh"
