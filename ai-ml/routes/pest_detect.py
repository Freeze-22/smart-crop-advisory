from flask import Blueprint, request, jsonify
from PIL import Image
import numpy as np
import json
import io
import tensorflow as tf


tflite = tf.lite


pest_bp = Blueprint('pest', __name__)

interpreter = tflite.Interpreter(model_path='models/pest_model.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

with open('models/class_labels.json', 'r') as f:
    class_labels = json.load(f)

@pest_bp.route('/api/pest/detect', methods=['POST'])
def detect_pest():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    img = Image.open(io.BytesIO(file.read())).resize((224, 224))
    img_array = np.array(img, dtype=np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()

    predictions = interpreter.get_tensor(output_details[0]['index'])[0]
    top_index = np.argmax(predictions)
    confidence = round(float(predictions[top_index]) * 100, 2)
    disease = class_labels[str(top_index)]

    return jsonify({
        "disease": disease,
        "confidence": confidence
    })
