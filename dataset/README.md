Instrucciones para construir el dataset (YOLO format)

1) Estructura esperada

dataset/
  raw/
    images/   <-- todas las imágenes originales (.jpg/.png)
    labels/   <-- archivos .txt con las anotaciones YOLO (misma base name)
  images/
    train/
    val/
    test/
  labels/
    train/
    val/
    test/

2) Clases
Crear `data/dataset.yaml` con las clases:

names:
  0: celular
  1: teclado

3) Herramientas de anotación
- Usar LabelImg y escoger el formato `YOLO`.
- Cada etiqueta generará un `.txt` con la línea: `class x_center y_center width height` (normalizado 0..1).

4) División
Usar el script `scripts/split_dataset.py --src dataset/raw --dest dataset` para dividir en train/val/test.

5) Recomendaciones
- Recolecta mínimo ~300 imágenes por clase si es posible; para el examen 100-200 puede ser aceptable.
- Aumenta variación: distintos ángulos, iluminación, fondos, objetos parciales.

6) Descarga automática de imágenes

Puedes usar el script `scripts/download_images.py` para descargar imágenes desde Bing automáticamente. Ejemplo:

```bash
python scripts/download_images.py --classes "celular,teclado" --num 200
```

Esto colocará las imágenes en `dataset/raw/images`. Revisa y elimina imágenes irrelevantes antes de anotar.
