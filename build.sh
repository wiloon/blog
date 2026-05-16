#!/bin/bash
set -e

count=$(find content/post -name "*.md" | wc -l | tr -d ' ')
chars=$(find content/post -name "*.md" -exec cat {} + | wc -m | tr -d ' ')
ts=$(date +%s)
mkdir -p static
echo "{\"article_count\":${count},\"total_chars\":${chars},\"generated_at\":${ts}}" \
  > static/stats.json
echo "article_count=${count}, total_chars=${chars}"

hugo --minify
