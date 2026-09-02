#!/usr/bin/env bash
# Regenera manifest.json a mano con lo que haya en esta carpeta.
# Usalo si querés previsualizar localmente antes de pushear (el GitHub
# Action hace esto mismo automáticamente al subir imágenes al repo).
set -euo pipefail
cd "$(dirname "$0")"

{
  echo "["
  first=1
  shopt -s nullglob nocaseglob
  for f in *.jpg *.jpeg *.png; do
    if [ "$first" = 1 ]; then first=0; else echo ","; fi
    printf '  "%s"' "$f"
  done
  echo ""
  echo "]"
} > manifest.json

echo "images/manifest.json actualizado:"
cat manifest.json
