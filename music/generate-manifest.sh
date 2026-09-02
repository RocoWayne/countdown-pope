#!/usr/bin/env bash
# Regenera manifest.json a mano con lo que haya en esta carpeta.
# El GitHub Action hace esto mismo automáticamente al subir música al repo.
set -euo pipefail
cd "$(dirname "$0")"

{
  echo "["
  first=1
  shopt -s nullglob nocaseglob
  for f in *.mp3 *.ogg *.wav *.m4a; do
    if [ "$first" = 1 ]; then first=0; else echo ","; fi
    printf '  "%s"' "$f"
  done
  echo ""
  echo "]"
} > manifest.json

echo "music/manifest.json actualizado:"
cat manifest.json
