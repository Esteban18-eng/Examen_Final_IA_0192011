#!/usr/bin/env bash
# Entrena usando Ultralytics YOLOv8 (necesitas instalar `ultralytics` en el virtualenv).

yolo task=detect mode=train model=yolov8n.pt data=data/dataset.yaml epochs=50 imgsz=640 project=models name=celular_teclado

# Al finalizar el mejor modelo se guardará en models/celular_teclado/weights/best.pt
