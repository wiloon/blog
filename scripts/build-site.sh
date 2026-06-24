#!/usr/bin/env sh
set -eu

HUGO_FLAGS="${HUGO_FLAGS:---minify}"
PAGEFIND_VERSION="${PAGEFIND_VERSION:-1.5.2}"

hugo ${HUGO_FLAGS}

if command -v pagefind >/dev/null 2>&1; then
  pagefind --site public
elif command -v npx >/dev/null 2>&1; then
  npx -y "pagefind@${PAGEFIND_VERSION}" --site public
else
  echo "error: pagefind not found (install binary or Node.js npx)" >&2
  exit 1
fi
