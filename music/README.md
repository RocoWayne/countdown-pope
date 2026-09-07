# Música de fondo

Poné acá los temas que quieras usar en el countdown (`../countdown.html`).
**Sin regla de nombre**: cualquier `.mp3`, `.ogg`, `.wav` o `.m4a` que haya
en esta carpeta se agrega a la playlist. Se reproduce siempre en orden
aleatorio (shuffle) y nunca se repite un tema hasta que sonaron todos los
demás — incluido el borde entre una vuelta y la siguiente.

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
- Los navegadores bloquean el autoplay CON sonido sin interacción previa,
  pero el autoplay muteado siempre está permitido. La página arranca el
  primer tema muteado a propósito y le saca el mute apenas confirma que
  empezó a sonar, así la música arranca sola, con sonido, sin necesitar
  ningún click. Si igual quedara bloqueada (política muy estricta del
  navegador), el botón de silenciar/activar (arriba a la izquierda)
  destraba el audio con el primer click.
- En OBS, además, activá "Control audio via OBS" en las propiedades de la
  fuente de Navegador — así el audio pasa por el mezclador de OBS en vez
  de depender del bloqueo de autoplay del navegador embebido.
