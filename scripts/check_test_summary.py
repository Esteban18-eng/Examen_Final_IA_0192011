from ultralytics import YOLO
import os
model = YOLO('models/best.pt')
for fname in sorted(os.listdir('dataset/images/test')):
    if not fname.lower().endswith(('.jpg','.jpeg','.png')):
        continue
    path = os.path.join('dataset/images/test', fname)
    r = model.predict(source=path, imgsz=640, conf=0.01, verbose=False)
    boxes = r[0].boxes
    confs = [float(b.conf) for b in boxes]
    if confs:
        print(fname, len(boxes), min(confs), max(confs), confs[:5])
    else:
        print(fname, 0)
