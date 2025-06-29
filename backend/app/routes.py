from flask import request, jsonify
import cv2
import numpy as np
import json
from .recognition import recognize_faces_in_boxes

def configure_routes(app):
    @app.route("/upload", methods=["POST"])
    def upload():
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']
        img_bytes = file.read()
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({"error": "Invalid image"}), 400

        boxes = []
        if 'boxes' in request.form:
            try:
                boxes = json.loads(request.form['boxes'])
            except Exception as e:
                return jsonify({"error": "Invalid boxes JSON", "details": str(e)}), 400
            
        results = recognize_faces_in_boxes(frame, boxes)

        return jsonify(results)
    
    @app.route("/", methods=["GET"])
    def home():
        return "Servidor corriendo correctamente ✅"