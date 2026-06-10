from ultralytics import YOLO
import os
model = YOLO('models/best.pt')
for fname in sorted(os.listdir('dataset/images/test')):
    if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue
    path = os.path.join('dataset/images/test', fname)
    results = model.predict(source=path, imgsz=640, conf=0.001, verbose=False)
    r = results[0]
    print('FILE', fname)
    try:
        for box in r.boxes:
            print(' box', box.cls, box.conf, box.xyxy)
    except Exception as e:
        print(' boxes error', e)
    print(' raw boxes', r.boxes)
    print(' preds', r.boxes.data if hasattr(r.boxes, 'data') else None)
    print('---')
