from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO('yolov8n.pt')
    model.train(
        data='data/dataset.yaml',
        epochs=50,
        imgsz=640,
        batch=2,
        workers=0,
        project='models',
        name='celular_teclado'
    )
