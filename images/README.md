# Imágenes de fondo del Papa

Poné acá las fotos que quieras usar en el countdown (`../countdown.html`).
**No hay ninguna regla de nombre**: cualquier `.jpg`, `.jpeg` o `.png` que
haya en esta carpeta se va a usar, en orden alfabético.

## Cómo funciona

La página no lee la carpeta directamente (un sitio estático no puede
"listar" un directorio) — lee `manifest.json`, un archivo con la lista de
imágenes que hay acá. Ese archivo se regenera solo:

- **Al pushear a GitHub**: el workflow `.github/workflows/update-image-manifest.yml`
  detecta cualquier cambio en `/images` (agregar o borrar una imagen) y
  reescribe `manifest.json` automáticamente, sin que tengas que hacer nada.
- **En local, antes de pushear**: si querés previsualizar antes de subir
  los cambios, corré `images/generate-manifest.sh` (o simplemente pusheá
  y esperá unos segundos a que corra el Action).

## Notas

- Si la carpeta queda vacía, el countdown sigue funcionando igual, solo
  que el panel lateral queda liso (sin foto).
- Formato recomendado: orientación vertical o cuadrada, mínimo ~1000px de
  ancho, para que se vea bien en el panel lateral.
- No edites `manifest.json` a mano salvo que sepas lo que hacés — se
  sobreescribe solo.
