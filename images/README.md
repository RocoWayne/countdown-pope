# Imágenes de fondo del Papa

Poné acá las fotos que quieras usar en el countdown (`countdown.html`).
La página las detecta y las usa automáticamente, en orden, sin tocar código.

## Convención de nombres

Nombrá cada archivo `pope-XX.<extensión>`, con `XX` de `01` a `20`:

```
images/pope-01.jpg
images/pope-02.png
images/pope-03.webp
...
images/pope-20.jpg
```

- Extensiones soportadas: `jpg`, `jpeg`, `png`, `webp`.
- No hace falta usar todos los números ni que sean consecutivos: podés
  tener solo `pope-01.jpg` y `pope-05.png`, por ejemplo — la página prueba
  del 01 al 20 y usa las que encuentre, en ese orden.
- Si no hay ninguna imagen, el countdown sigue funcionando igual, solo que
  el panel de fondo queda liso (sin foto).
- Formato recomendado: orientación vertical o cuadrada, mínimo ~1000px de
  ancho, para que se vea bien en el panel lateral.

No hace falta editar `countdown.html` al agregar o sacar fotos de esta
carpeta.
