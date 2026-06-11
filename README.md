# Examen Final – Detección de Objetos con YOLO (YOLOv8)

Aplicación de visión por computadora para detección por imágenes, entrenada con un dataset propio etiquetado en formato YOLO.

---

## 1. Objetivo del proyecto

Desarrollar un sistema capaz de detectar al menos dos (2) categorías en imágenes usando YOLOv8, aplicando el flujo completo: colección y etiquetado del dataset, entrenamiento, evaluación con métricas estándar y despliegue en una aplicación web (Flask).

---

## 2. Categorías detectadas

El modelo está preparado para detectar las siguientes clases:

- `celular`
- `teclado`

La configuración de clases se encuentra en `data/dataset.yaml` (campo `names`).

---

## 3. Construcción del dataset

### 3.1 Formato y anotaciones

- Todas las anotaciones usan el formato YOLO: archivos `.txt` con líneas `class x_center y_center width height` (coordenadas normalizadas).

### 3.2 Organización

- Coloca las imágenes originales en `dataset/raw/images/` y las etiquetas en `dataset/raw/labels/`.
- Usa `scripts/split_dataset.py` para generar las carpetas finales:
  - `dataset/train/images`, `dataset/train/labels`
  - `dataset/val/images`, `dataset/val/labels`
  - `dataset/test/images`, `dataset/test/labels`

### 3.3 Herramientas de apoyo

- `scripts/download_images.py` — descarga imágenes desde web (se usó para pruebas).
- `scripts/split_dataset.py` — divide el raw en train/val/test.
- `scripts/validate_dataset.py` — chequeos básicos (archivos sin etiqueta, formatos, etc.).

---

## 4. Entrenamiento del modelo

### 4.1 Modelo base

- Se puede usar `yolov8n.pt` o `yolov8s.pt` como punto de partida (weights oficiales de Ultralytics).

### 4.2 Script de entrenamiento

- Entrenamiento principal: `scripts/train.py`.

Ejemplo de ejecución (ajusta `--epochs` y `--batch` según tu máquina):

```bash
python scripts/train.py --data data/dataset.yaml --epochs 50 --batch 4
```

### 4.3 Salidas

- Resultados y pesos se guardan en `runs/detect/<nombre-experimento>/weights/best.pt`.
- Copia `best.pt` a `models/best.pt` para que la app lo use.

---

## 5. Evaluación

Se recomienda evaluar con las métricas estándar de detección:

- Precision
- Recall
- mAP@50
- mAP@50-95

Comando rápido con Ultralytics:

```bash
python -c "from ultralytics import YOLO; YOLO('models/best.pt').val(data='data/dataset.yaml')"
```

Incluye generar curvas y, si es posible, matriz de confusión para inspección.

---

## 6. Aplicación (Flask)

La aplicación está en `app/app.py` y permite subir una imagen para inferencia. Características principales:

- Carga automática de `models/best.pt`.
- Input para ajustar el umbral de confianza desde la UI.
- Filtrado de cajas muy pequeñas para reducir falsos positivos.

Ejecutar la app (desde la raíz del repo):

```powershell
python .\app\app.py
```

Abrir en el navegador: `http://127.0.0.1:5000/`.

---

## 7. Instrucciones rápidas de uso

1. Instala dependencias:

```bash
pip install -r requirements.txt
```

2. Prepara dataset y divide:

```bash
python scripts/split_dataset.py --src dataset/raw --dest dataset
```

3. Entrena (ejemplo):

```bash
python scripts/train.py --data data/dataset.yaml --epochs 50 --batch 4
```

4. Ejecuta la app:

```powershell
python .\app\app.py
```

5. Abre `http://127.0.0.1:5000/` y sube imágenes para probar.

---

## 8. Evidencias y resultados

- Guarda capturas de entrenamiento, curvas y matrices en `Evidencias/`.
- El modelo entrenado en este repositorio se guardó en `runs/detect/models/celular_teclado-5/weights/best.pt` y se copió a `models/best.pt`.

---

## 9. Recomendaciones finales

- Si observas falsos positivos frecuentes: añade imágenes negativas al dataset y vuelve a entrenar.
- Revisa etiquetas manualmente con `labelImg` si notas anotaciones incorrectas.
- Para la presentación, muestra la ejecución en la app y alguna gráfica de métricas (Precision/Recall/mAP).

---

## 10. Archivos importantes

- `README.md` — este documento
- `data/dataset.yaml` — configuración del dataset
- `scripts/train.py` — script de entrenamiento
- `app/app.py` — aplicación Flask
- `requirements.txt` — dependencias
- `Evidencias/` — carpeta para capturas y gráficos


# Examen Final — Detección de Objetos con YOLO

Proyecto: detección de `celular` y `teclado` usando YOLO y despliegue con Flask.

Contenido del repositorio:
- `dataset/` — instrucciones y estructura para imágenes y anotaciones (YOLO format).
- `data/dataset.yaml` — configuración del dataset para Ultralytics YOLO.
- `scripts/split_dataset.py` — script para dividir dataset en train/val/test.
- `models/` — aquí se guardará el modelo entrenado (`best.pt`).
- `app/app.py` — aplicación Flask para subir imágenes y visualizar detecciones.
- `requirements.txt` — dependencias Python.
- `train.sh` — comando ejemplo para entrenar con Ultralytics YOLOv8.

Pasos rápidos:
1. Recolecta imágenes para ambas clases y colócalas en `dataset/raw/images` y las etiquetas (mismo nombre, extensión `.txt`) en `dataset/raw/labels` en formato YOLO.
2. Anota con LabelImg (formato YOLO) si no tienes etiquetas.
3. Ejecuta `python scripts/split_dataset.py --src dataset/raw --dest dataset` para crear `images/labels` divididos.
4. Entrena con:

```bash
bash train.sh
```

5. Ejecuta la app Flask para probar cargas:

```bash
python app/app.py
```

## Estado actual
- El modelo fue entrenado en `runs/detect/models/celular_teclado-5/weights/best.pt`.
- El peso final se copió a `models/best.pt`.
- Se generó una imagen de prueba en `models/demo_result.jpg`.

## Cómo probar la aplicación
1. Activa el entorno virtual:

```powershell
venv\Scripts\activate
```

2. Ejecuta el servidor Flask:

```powershell
python app/app.py
```

3. Abre el navegador en `http://127.0.0.1:5000`.
4. Sube una imagen y revisa la detección.

> Nota: este entrenamiento usó etiquetas automáticas basadas en el nombre del archivo para una prueba rápida. Para mejor rendimiento real, anota cada imagen manualmente en `dataset/raw/labels` con `labelImg` y vuelve a entrenar.
