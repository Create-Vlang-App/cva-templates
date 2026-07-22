#!/usr/bin/env bash
# Some VPM installs land as ~/.vmodules/foo.bar instead of ~/.vmodules/foo/bar.
set -euo pipefail
VM="${VMODULES:-$HOME/.vmodules}"
shopt -s nullglob
for dotted in "$VM"/*.*; do
  [[ -d "$dotted" ]] || continue
  base=$(basename "$dotted")
  [[ "$base" == *.* ]] || continue
  parent="${base%%.*}"
  child="${base#*.}"
  [[ "$child" == *.* ]] && continue
  target="$VM/$parent/$child"
  mkdir -p "$VM/$parent"
  if [[ ! -e "$target" ]]; then
    ln -sfn "$dotted" "$target"
    echo "normalized $base -> $parent/$child"
  fi
done
