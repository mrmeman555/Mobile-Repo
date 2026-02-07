#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
index_file="${script_dir}/INDEX.md"

if [[ $# -gt 0 ]]; then
  input="$*"
else
  input="$(cat)"
fi

# Trim-only check (don't accept empty context)
if [[ -z "${input//[[:space:]]/}" ]]; then
  echo "Error: no context text provided." >&2
  echo "Usage: ./append_context.sh \"text here\"  (or pipe via stdin)" >&2
  exit 1
fi

timestamp="$(date -u +"%Y%m%d_%H%M%S")"
fname="${timestamp}.md"
out_file="${script_dir}/${fname}"

printf "%s\n" "${input}" > "${out_file}"

# Derive a non-empty first line for the index description (excerpt, not a rewrite).
first_line="$(
  printf "%s\n" "${input}" \
  | awk 'NF{print; exit}'
)"

# If INDEX still has placeholder, remove it on first append.
if [[ -f "${index_file}" ]] && grep -q "^- (no entries yet)$" "${index_file}"; then
  tmp="${index_file}.tmp"
  grep -v "^- (no entries yet)$" "${index_file}" > "${tmp}"
  mv "${tmp}" "${index_file}"
fi

# Truncate excerpt for index readability.
excerpt="${first_line:0:120}"

printf -- "- %s — %s\n" "${fname}" "${excerpt}" >> "${index_file}"

printf "%s\n" "${fname}"

