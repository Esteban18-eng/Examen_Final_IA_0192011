import os
import shutil
from ultralytics import YOLO
from PIL import Image

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    src = os.path.join('runs', 'detect', 'models', 'celular_teclado-5', 'weights', 'best.pt')
    dst = os.path.join('models', 'best.pt')
    if os.path.exists(src):
        shutil.copy(src, dst)
        print('Copied best.pt to', dst)
    else:
        print('Model source not found:', src)
        raise SystemExit(1)
    test_dir = os.path.join('dataset', 'images', 'test')
    imgs = [f for f in os.listdir(test_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not imgs:
        raise SystemExit('No test images found')
    img_path = os.path.join(test_dir, imgs[0])
    model = YOLO(dst)
    results = model.predict(source=img_path, imgsz=640)
    res = results[0]
    out = res.plot()
    Image.fromarray(out).save(os.path.join('models', 'demo_result.jpg'))
    print('Saved demo_result.jpg for', img_path)
