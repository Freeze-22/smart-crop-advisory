from flask import Blueprint, request, jsonify
from PIL import Image
import numpy as np
import tensorflow as tf
import json
import io

pest_bp = Blueprint('pest', __name__)

model = tf.keras.models.load_model('models/pest_model.h5')

with open('models/class_labels.json', 'r') as f:
    class_labels = json.load(f)

@pest_bp.route('/api/pest/detect', methods=['POST'])
def detect_pest():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    img = Image.open(io.BytesIO(file.read())).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    top_index = np.argmax(predictions[0])
    confidence = round(float(predictions[0][top_index]) * 100, 2)
    disease = class_labels[str(top_index)]

    return jsonify({
        "disease": disease,
        "confidence": confidence
    })