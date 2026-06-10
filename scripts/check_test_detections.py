from ultralytics import YOLO
import os

model = YOLO('models/best.pt')
for f in sorted(os.listdir('dataset/images/test')):
    if not f.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    path = os.path.join('dataset/images/test', f)
    r = model.predict(source=path, imgsz=640, conf=0.25)
    boxes = r[0].boxes
    print(f, len(boxes), [b.tolist() for b in boxes.xyxy] if len(boxes) else [])
