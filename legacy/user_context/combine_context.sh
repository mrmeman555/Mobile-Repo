#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
out="${script_dir}/combined_user_context.md"

readme="${script_dir}/README.md"
index="${script_dir}/INDEX.md"

tmp="${out}.tmp"
: > "${tmp}"

cat "${readme}" >> "${tmp}"
printf "\n\n" >> "${tmp}"
cat "${index}" >> "${tmp}"
printf "\n\n" >> "${tmp}"

# Chronological order by timestamped filename (lexicographic sort).
files="$(
  ls -1 "${script_dir}"/*.md 2>/dev/null \
  | awk -v r="${readme}" -v i="${index}" -v o="${out}" '
      $0 != r && $0 != i && $0 != o { print }
    ' \
  | sort
)"

if [[ -n "${files}" ]]; then
  while IFS= read -r f; do
    printf "\n\n" >> "${tmp}"
    cat "${f}" >> "${tmp}"
  done <<< "${files}"
fi

mv "${tmp}" "${out}"
printf "%s\n" "${out}"

