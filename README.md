# Countdown Visita del Papa a la Argentina

Página única (`countdown.html`) pensada como fuente de navegador de OBS
para transmitir en vivo la cuenta regresiva a la visita de León XIV a la
Argentina. Sin build, sin dependencias — se sirve tal cual desde GitHub
Pages (`index.html` redirige a `countdown.html`).

## Contenido editable sin tocar código

Estas carpetas/archivos se editan directo, sin necesidad de tocar el HTML:

- **`/images`** — fotos de fondo del carrusel. Ver `images/README.md`.
- **`/music`** — música de fondo. Ver `music/README.md`.
- **`trivia.json`** — datos que rotan en la caja "¿Sabías que…?" (array
  plano de strings, máx. 240 caracteres cada uno).
- **`cta.json`** — preguntas del popup "Participá" que invita a comentar
  en el chat (mismo formato que `trivia.json`).

El botón de silenciar música (arriba a la izquierda) siempre arranca en
"sonido activado" cada vez que se carga la página — el mute es una
acción opcional del usuario, a propósito no se guarda entre cargas para
que la transmisión nunca arranque en silencio por accidente.

La página vuelve a leer estos cuatro archivos sola cada 24 horas
(`CONTENT_REFRESH_MS`), así que el contenido nuevo se refleja en una
transmisión ya en vivo sin tener que reiniciar la fuente de OBS a mano.

## Modo "el Papa ya llegó" (pantalla de llegada)

Cuando el countdown llega a cero, la página cambia de estado **sin
recargar ni redireccionar** — todo pasa dentro del mismo documento para
no cortar la música ni perder las fotos ya cargadas.

**Cómo se activa:** `tick()` detecta que `TARGET_DATE - ahora <= 0` y
llama a `activateArrivalMode()` (función idempotente: solo actúa la
primera vez). Esa función agrega la clase `papal-arrival-mode` al
`<body>`, que dispara todo el cambio visual por CSS.

**Qué cambia en pantalla:**
- El panel de fotos (`.photo-panel`) pasa de 42vw a ocupar el 100% del
  ancho, con una transición suave (`transition: width 1.2s ease`).
- Aparece un degradado oscuro arriba del carrusel (en vez del degradado
  blanco lateral que usa en modo countdown), para que el texto se lea
  bien encima de cualquier foto.
- Se muestra el mensaje grande centrado (`#arrivalMessage`):
  **"¡EL PAPA LEÓN YA ESTÁ EN ARGENTINA!"** / *"Cobertura exclusiva en
  canal26.com"*, con un fundido de entrada (`opacity` + `transition`).
- Se ocultan el bloque de contenido normal (título, countdown, caja de
  trivia) y el popup de chat "Participá" (`display: none !important`).
- El logo del canal y el botón de silenciar/activar música **siguen
  visibles** (viven fuera de `.content`, no se tocan).
- La música sigue sonando sin cortes: el `<audio>` nunca se toca al
  cambiar de modo.

**Detalles de pulido (ajustados para que se vea bien en pantalla
completa, no solo en el panel angosto):**
- La barra roja fina que separa el panel de fotos del contenido
  (`.photo-panel::after`) se oculta en este modo — era un acento pensado
  para el panel lateral de 42vw; en pantalla completa quedaba como una
  línea suelta pegada al borde izquierdo, sin sentido visual.
- El encuadre de las fotos cambia de `background-position: center 20%`
  (que fuerza la parte superior de la imagen, pensado para un panel más
  alto que ancho) a `center center` — centra la imagen entera, mejor
  encuadre para el formato 16:9 completo de la pantalla de llegada.

**Limpieza de recursos:** como este modo no tiene vuelta atrás (una vez
que el Papa llegó, no hay countdown al que volver), `activateArrivalMode()`
también frena los timers que ya no tienen nada que mostrar: el `tick()`
del countdown, la rotación de trivia y el ciclo del popup de chat. Así no
quedan corriendo de fondo para siempre sin ningún efecto visible.

**Cómo probarlo sin esperar a la fecha real — modo `?arrived=1`:** abrir
la página con ese parámetro en la URL, por ejemplo:

```
countdown.html?arrived=1
```

o, ya publicado en GitHub Pages, algo como
`https://<usuario>.github.io/countdown-pope/countdown.html?arrived=1`.
Fuerza el modo de llegada apenas carga la página (ver `FORCE_ARRIVED` en
`CONFIGURACIÓN`), sin tocar `TARGET_DATE` ni necesitar la consola del
navegador — cómodo para que cualquiera del equipo revise el look antes
del evento, no solo quien sabe abrir DevTools. Sacar el `?arrived=1` de
la URL vuelve al countdown normal.

**Alternativa por consola** (si prefieren no tocar la URL): abrir
`countdown.html`, esperar unos segundos a que carguen música y fotos,
abrir la consola (F12) y ejecutar `TARGET_DATE.setTime(Date.now() - 1000)`.
Ninguna de las dos formas modifica el archivo ni el repositorio.

## Hardening para transmisiones largas (60+ días corridos)

- **Tope de memoria en el carrusel** (`MAX_BG_LAYERS = 20`): al superar
  el tope, se sacan del DOM las fotos más viejas.
- **Timeout de red** (`FETCH_TIMEOUT_MS = 15000`): todos los `fetch()` de
  manifests/trivia/cta y la carga de cada imagen se cortan solos si
  tardan de más, para que un cuelgue puntual no bloquee el resto.
- **Freno anti-loop en música** (`MUSIC_ERROR_BACKOFF_MS = 30000`): si
  fallan todos los temas de la playlist seguidos, espera antes de
  reintentar en vez de reintentar sin parar.
- **Música se corta si vacían `music/manifest.json`** a propósito, en vez
  de quedar sonando para siempre lo último que había en memoria.
- **Logs de diagnóstico** en la consola del navegador (prefijo
  `[countdown]`) para poder diagnosticar a distancia si algo falla en una
  transmisión larga.

## Cómo editar la fecha objetivo

Buscar la constante `TARGET_DATE` en el bloque `CONFIGURACIÓN` del
`<script>` de `countdown.html` (formato ISO con offset de Buenos Aires,
`-03:00`).
