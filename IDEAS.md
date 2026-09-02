# Ideas a futuro (sin implementar todavía)

Notas de una charla sobre cómo reaprovechar la arquitectura de este
countdown en otros proyectos de transmisión 24/7. No se aplicó ningún
cambio al código a partir de esto — es solo el registro de la idea para
retomarla más adelante.

## Lo que ya es reutilizable tal cual (el "motor" de este proyecto)

- **Contenido editable sin build, sin nombres fijos**: carpeta +
  `manifest.json` regenerado por GitHub Action al pushear (ver `/images`,
  `/music`). Sirve para cualquier activo que alguien no técnico tenga que
  poder subir directo al repo sin tocar código.
- **Refresh periódico sin cortar nada**: patrón `refreshX()` que se puede
  volver a llamar sin interrumpir lo que ya está sonando/mostrándose
  (música sigue, imágenes se suman, texto se actualiza recién en el
  próximo ciclo). Es la pieza central para cualquier fuente de OBS que
  viva semanas sin reiniciarse, porque la fuente de navegador nunca se
  refresca sola.
- **Shuffle sin repetición consecutiva** (`shuffle()` + `buildXOrder(avoidFirst)`):
  genérico para música, trivia, CTAs, o titulares — cualquier lista que
  se muestre en loop sin que se note la repetición.
- **Hardening para 60+ días corridos**: timeout de fetch, tope de memoria
  en elementos que se acumulan en el DOM, backoff cuando algo falla en
  loop, logs con prefijo reconocible en consola. Aplica a cualquier
  gráfica "always-on", no es específico de este proyecto — conviene
  tenerlo de entrada en el próximo, no agregarlo después.
- **Cambio de estado sin redirect** (`activateArrivalMode()`): clase en
  `<body>`, todo dentro del mismo documento, sin recargar. Patrón
  genérico para "la transmisión cambia de fase" (resultados electorales,
  un evento que pasa de "arrancamos en instantes" a cobertura en vivo,
  una campaña que llega a la meta).

## Proyecto concreto: canal de noticias 24/7 (RSS + música)

Idea: un stream con música de fondo (mismo sistema que este proyecto) más
un feed de noticias en vivo alimentado por RSS.

- **RSS en vez de scraper de HTML**: antes de este proyecto existió un
  scraper de canal26.com con su propio Action cada 20 min, generando
  `news.json` — funcionó en un run real, pero se descartó. Un RSS es más
  robusto porque es un contrato estable (no se rompe si el sitio cambia
  el HTML), a diferencia del scraper.
- **Mismo esqueleto que `update-image-manifest.yml` /
  `update-music-manifest.yml`**: Action con cron que golpea el feed RSS,
  parsea los ítems, escribe `news.json`, comitea con el mismo loop de
  "fetch + rebase + retry" para evitar choques de push.
- **Refresh mucho más frecuente**: para noticias en vivo,
  `CONTENT_REFRESH_MS` tendría que bajar a minutos (no 24hs como acá) —
  el patrón ya lo soporta, es cambiar la constante. Ahí el hardening
  (timeout, backoff) importa más porque el fetch se repite mucho más
  seguido.
- **Ticker inferior en vez de caja rotativa**: para noticias tiene más
  sentido un scroll horizontal continuo (estilo zócalo de noticiero) que
  una caja que cambia cada 45 segundos. El CSS/JS del `.zocalo` que se
  sacó de este mismo repo sigue existiendo en el historial de git —
  se puede recuperar como punto de partida en vez de escribirlo de cero.
- **Filtrado/prioridad**: un RSS trae muchos ítems; convendría filtrar
  por antigüedad (últimas N horas) o marcar "urgente" de alguna forma
  para no mostrar noticias viejas en un stream 24/7.
- **Modo "última hora"**: mismo patrón de `activateArrivalMode()` pero
  disparado por contenido (una noticia marcada urgente en el RSS) en vez
  de por una fecha — reemplaza momentáneamente el layout normal.

## Cómo estructurarlo cuando se retome

Separar el "motor" (manifest pattern, refresh, shuffle, hardening) de lo
específico de cada evento (layout, countdown, mensaje de llegada) — por
ejemplo clonando este `countdown.html` como plantilla base y reemplazando
solo el layout y las fuentes de contenido, sin tocar la lógica de
refresh/hardening ya probada.
