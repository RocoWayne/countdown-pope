# Música de fondo

Poné acá los temas que quieras usar en el countdown (`../countdown.html`).
**Sin regla de nombre**: cualquier `.mp3`, `.ogg`, `.wav` o `.m4a` que haya
en esta carpeta se agrega a la playlist, en orden alfabético, y se
reproducen uno atrás del otro en loop.

Usá solo música libre de derechos / con licencia que permita este uso
(ej. YouTube Audio Library, Pixabay Music, Free Music Archive con licencia
CC adecuada) — la responsabilidad de la licencia es de quien sube el
archivo.

## Cómo funciona

Igual que `/images`: la página no puede "listar" una carpeta por sí sola,
así que lee `manifest.json`, que se regenera solo:

- **Al pushear a GitHub**: el workflow `.github/workflows/update-music-manifest.yml`
  detecta cualquier cambio acá y reescribe `manifest.json` automáticamente.
- **En local, antes de pushear**: corré `music/generate-manifest.sh` si
  querés previsualizar sin esperar al Action.

## Notas

- Si la carpeta está vacía, el countdown funciona igual, sin música.
- Los navegadores (y OBS) suelen bloquear el autoplay con sonido hasta que
  haya alguna interacción. La página maneja esto: si el autoplay es
  bloqueado, muestra un botón chico "🔊 Activar música" una sola vez.
  En OBS, activá "Control audio via OBS" en las propiedades de la fuente
  de Navegador para que no dependa de esto.
