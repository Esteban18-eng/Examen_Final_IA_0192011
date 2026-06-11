# Examen Final – Detección de Objetos con YOLO (YOLOv8)

Aplicación de visión por computadora para **detección por imágenes**, entrenada con un **dataset propio** etiquetado en formato YOLO.

---

## 1. Objetivo del proyecto

Desarrollar un sistema capaz de detectar al menos **dos (2) categorías** de objetos en imágenes usando **YOLOv8**, aplicando el flujo completo:

1. Construcción del dataset (recolección, etiquetado y división)
2. Entrenamiento del modelo
3. Evaluación con métricas (Precision, Recall, mAP@50, mAP@50-95)
4. Implementación de una aplicación funcional (Flask)

---

## 2. Categorías detectadas

El modelo está entrenado para **2 clases**:

- **celular**
- **teclado**

Configuración de clases:

- `nc: 2`
- `names: ['celular', 'teclado']`

---

## 3. Construcción del Dataset

### 3.1 Dataset y etiquetado

- Las imágenes fueron anotadas en **formato YOLOv8/YOLO** (archivos `.txt` con coordenadas normalizadas en formato: `class x_center y_center width height`).
- La estructura del dataset se organiza en:
  - `train/`
  - `val/`
  - `test/`

### 3.2 División del dataset

Se usa la configuración del `data/dataset.yaml`:

- `train: ../train/images`
- `val: ../val/images`
- `test: ../test/images`

### 3.3 Evidencias de entrenamiento / dataset

Se incluyen evidencias del proceso de entrenamiento y métricas en la carpeta **`Evidencias/`**.

Scripts de apoyo incluidos:
- `scripts/download_images.py` — descarga imágenes.
- `scripts/split_dataset.py` — divide el dataset en train/val/test.
- `scripts/validate_dataset.py` — valida integridad de anotaciones.

---

## 4. Entrenamiento del Modelo

### 4.1 Modelo base

Se utilizó YOLOv8 como modelo base:

- `yolov8n.pt` o `yolov8s.pt`

### 4.2 Script de entrenamiento

El entrenamiento se realiza con `scripts/train.py`:

- Dataset: `data='data/dataset.yaml'`
- Épocas: `epochs=50`
- Tamaño de imagen: `imgsz=640`
- Batch: `batch=4`
- Nombre de experimento: `name='celular_teclado'`

Comando de ejecución:

```bash
python scripts/train.py --data data/dataset.yaml --epochs 50 --batch 4
```

### 4.3 Evidencias del entrenamiento

Capturas incluidas en `Evidencias/`, por ejemplo:

- **Comienzo de entrenamiento**: `Evidencias/entrenamiento_inicio.png`
- Curvas/Gráficas del entrenamiento:
  - `Evidencias/BoxF1_curve.png`
  - `Evidencias/BoxP_curve.png`
  - `Evidencias/BoxR_curve.png`
  - `Evidencias/BoxPR_curve.png`
- Matriz de confusión:
  - `Evidencias/confusion_matrix_normalized.png`
  - `Evidencias/confusion_matrix.png`

---

## 5. Evaluación del Modelo

Durante la evaluación se analizan métricas típicas de YOLO:

### 5.1 Precision

**Precision** mide qué proporción de las detecciones realizadas por el modelo son correctas:

- Fórmula: `Precision = TP / (TP + FP)`
- Alta Precision ⇒ pocas falsas alarmas (detecciones incorrectas).
- Ejemplo: Si el modelo hace 100 detecciones y 95 son correctas, Precision = 0.95 (95%)

### 5.2 Recall

**Recall** mide qué proporción de los objetos reales fueron detectados por el modelo:

- Fórmula: `Recall = TP / (TP + FN)`
- Alta Recall ⇒ pocos objetos reales se pierden.
- Ejemplo: Si hay 100 objetos reales y el modelo detecta 85, Recall = 0.85 (85%)

### 5.3 mAP@50

**mAP@50** es el promedio del **Average Precision** sobre todas las clases usando:

- umbral de IoU = 0.50
- Se calcula el área bajo la curva Precision-Recall para cada clase.
- Se promedian los valores de todas las clases.
- Menos exigente que mAP@50-95 porque permite imprecisión en localización (mínimo 50%).

### 5.4 mAP@50-95

**mAP@50-95** es el promedio del AP para múltiples umbrales de IoU:

- IoU en el rango [0.50, 0.95] (paso típico 0.05)
- Más estricto que mAP@50 porque exige localización precisa (múltiples umbrales).
- Evalúa mejor la calidad general del modelo.
- Valores típicamente menores que mAP@50.

### 5.5 Evidencias de métricas

Se incluyen figuras en `Evidencias/`:

- **Salida de consola con métricas**: `Evidencias/metricas_evaluacion.png`
  - Valores de Precision, Recall, mAP@50, mAP@50-95

- **Curvas de Precision/Recall/F1**:
  - `Evidencias/BoxP_curve.png`
  - `Evidencias/BoxR_curve.png`
  - `Evidencias/BoxF1_curve.png`
  - `Evidencias/BoxPR_curve.png`

- **Matriz de confusión**:
  - `Evidencias/confusion_matrix_normalized.png`
  - `Evidencias/confusion_matrix.png`

- **Ejemplos de predicciones**:
  - `Evidencias/prediccion_correcta_1.jpg`
  - `Evidencias/prediccion_correcta_2.jpg`
  - `Evidencias/prediccion_error_1.jpg`

> Nota: Las cifras numéricas exactas (valores de Precision/Recall/mAP) dependen del reporte generado por Ultralytics para la corrida específica. Las evidencias visuales incluidas sustentan el análisis requerido.

---

## 6. Implementación de la Aplicación (Flask)

Se implementa una aplicación web con **Flask** que:

1. Permite cargar una imagen.
2. Ejecuta inferencia con el modelo entrenado.
3. Dibuja/guarda la salida y muestra las detecciones (clase + confianza).

### 6.1 Script principal

- `app/app.py`

Características:

- Carga del modelo entrenado: `YOLO('models/best.pt')`
- Formulario para subir imágenes: `POST /`
- Ajuste de umbral de confianza desde UI.
- Filtrado de cajas pequeñas por área.
- Render de la salida: template HTML dinámico.

### 6.2 Frontend

- Página HTML integrada en `app/app.py`.
- Formulario de carga de imagen.
- Visualización de detecciones (clase + confianza).

---

## 7. Instrucciones de ejecución

### 7.1 Requisitos

Ver `requirements.txt`.

Archivo `requirements.txt`:

- `ultralytics`
- `opencv-python`
- `flask`
- `numpy`
- `torch`

### 7.2 Instalación (entorno Python)

```bash
pip install -r requirements.txt
```

### 7.3 Ejecutar la aplicación Flask

```powershell
python .\app\app.py
```

Abrir el navegador en:

- `http://127.0.0.1:5000/`

### 7.4 Demostración de categorías

Durante la sustentación:

1. Ejecutar `python .\app\app.py`
2. Cargar una imagen de prueba donde aparezcan **celular** y/o **teclado**.
3. Ver las detecciones mostradas en pantalla (lista de clases y porcentaje de confianza).
4. Ajustar el umbral de confianza si es necesario.

---

## 8. Estructura del proyecto

- `scripts/train.py` → script de entrenamiento
- `scripts/download_images.py` → descarga de imágenes
- `scripts/split_dataset.py` → división de dataset
- `scripts/validate_dataset.py` → validación de dataset
- `app/app.py` → aplicación Flask de inferencia por imagen
- `data/dataset.yaml` → configuración del dataset y clases
- `Evidencias/` → capturas de curvas, métricas y matrices de evaluación
- `models/best.pt` → peso del modelo entrenado (usado por la app)
- `runs/` → carpeta de salidas de entrenamiento e inferencia
- `dataset/` → carpeta del dataset (train/val/test con images/labels)
- `requirements.txt` → dependencias del proyecto

---

## 9. Sustentación técnica (qué decir en la demostración en el salon)

1. **Ejecución del sistema**: Iniciar la app con `python .\app\app.py`.

2. **Detección de las categorías entrenadas**: Mostrar que la app detecta **celular** y **teclado**.

3. **Explicar el dataset utilizado**:
   - Se etiquetó en formato YOLO.
   - Se dividió en `train/`, `val/`, `test/` usando `data/dataset.yaml`.

4. **Explicar métricas obtenidas**: Definir y diferenciar:
   - Precision: proporción de detecciones correctas.
   - Recall: proporción de objetos reales detectados.
   - mAP@50: métrica promedio con IoU 0.50 (menos exigente).
   - mAP@50-95: métrica promedio con múltiples IoU (más estricto).

5. **Apoyar con evidencias visuales**:
   - Capturas de curvas: `BoxP_curve`, `BoxR_curve`, `BoxF1_curve`, `BoxPR_curve`.
   - Matriz de confusión: `confusion_matrix_normalized`.
   - Ejemplos de predicciones correctas e incorrectas.

6. **Explicación general de la arquitectura**:
   - Se usa YOLOv8 (backbone + neck + head para detección).
   - El modelo aprende a predecir bounding boxes y clases simultáneamente.
   - En inferencia, Flask carga `best.pt` y ejecuta `model(image, conf=..., iou=...)`.

7. **Robustez del sistema**: Mostrar resultados en varias imágenes del conjunto `test/` o imágenes similares.

---

## 10. Modelo entrenado

El modelo final se encuentra en:

- `models/best.pt` (copia de trabajo para la app)
- `runs/detect/<nombre-experimento>/weights/best.pt` (salida original del entrenamiento)

---

## 11. Archivos importantes

- `README.md`
- `data/dataset.yaml`
- `scripts/train.py`
- `app/app.py`
- `requirements.txt`
- Evidencias: `Evidencias/*`
