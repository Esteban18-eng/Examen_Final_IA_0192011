from flask import Flask, request, render_template_string, send_file
from ultralytics import YOLO
import os
import cv2
import tempfile
import numpy as np

app = Flask(__name__)
MODEL_PATH = os.path.join('models','best.pt')
MODEL_CONFIDENCE = 0.6

if os.path.exists(MODEL_PATH):
    model = YOLO(MODEL_PATH)
else:
    model = None

HTML = '''
<!doctype html>
<title>Detección: celular y teclado</title>
<h1>Sube una imagen</h1>
<form method=post enctype=multipart/form-data>
    <input type=file name=file>
    <label for="conf">Umbral confianza:</label>
    <input id="conf" name="conf" type="number" min="0" max="1" step="0.01" value="{{default_conf}}">
    <input type=submit value=Subir>
</form>
{% if img_url %}
  <h2>Resultado</h2>
  <p><strong>Detecciones:</strong> {{count}}</p>
    {% if detections %}
        <ul>
        {% for d in detections %}
            <li>{{d.name}} ({{'%.2f'|format(d.conf)}})</li>
        {% endfor %}
        </ul>
    {% endif %}
  <img src="{{img_url}}" style="max-width:90%">
{% endif %}
'''

@app.route('/', methods=['GET','POST'])
def index():
    img_url = None
    count = None
    detections = []
    selected_conf = MODEL_CONFIDENCE
    if request.method == 'POST':
        f = request.files.get('file')
        if not f:
            return 'No file', 400
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        f.save(tmp.name)
        if model is None:
            return 'Modelo no encontrado en models/best.pt. Entrena y coloca el modelo allí.', 500
        # allow overriding the confidence from the form
        try:
            selected_conf = float(request.form.get('conf', MODEL_CONFIDENCE))
        except Exception:
            selected_conf = MODEL_CONFIDENCE
        results = model.predict(source=tmp.name, imgsz=640, conf=selected_conf, iou=0.45)
        res = results[0]
        count = len(res.boxes)
        detections = []
        # determine image size to compute box area threshold
        h = w = None
        if hasattr(res, 'orig_shape') and res.orig_shape is not None:
            try:
                h, w = int(res.orig_shape[0]), int(res.orig_shape[1])
            except Exception:
                h = w = None
        if h is None or w is None:
            img_cv = cv2.imread(tmp.name)
            if img_cv is not None:
                h, w = img_cv.shape[:2]
        if h is None or w is None:
            h, w = 640, 640
        min_area = 0.002 * (w * h)
        for row in res.boxes.data:
            x1, y1, x2, y2, conf, cls = [float(x) for x in row[:6]]
            area = max(0.0, (x2 - x1)) * max(0.0, (y2 - y1))
            if area < min_area:
                continue
            detections.append({
                'name': model.names[int(cls)],
                'conf': float(conf)
            })
        img = res.plot()
        out_tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        cv2.imwrite(out_tmp.name, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        img_url = '/result/' + os.path.basename(out_tmp.name)
    return render_template_string(HTML, img_url=img_url, count=count, detections=detections if request.method == 'POST' else [], default_conf=selected_conf)

@app.route('/result/<filename>')
def result_file(filename):
    path = os.path.join(tempfile.gettempdir(), filename)
    if os.path.exists(path):
        return send_file(path, mimetype='image/jpeg')
    return 'Not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
