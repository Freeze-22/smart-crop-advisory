from flask import Blueprint, request, jsonify
import pickle
import numpy as np

ml_bp = Blueprint('ml', __name__)

# Load model and encoder once at startup
with open('crop_model.pkl', 'rb') as f:
    crop_model = pickle.load(f)

with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

@ml_bp.route('/api/ml/recommend-crop', methods=['POST'])
def recommend_crop():
    data = request.get_json()

    try:
        features = np.array([[
            data['n'],
            data['p'],
            data['k'],
            data['temperature'],
            data['humidity'],
            data['ph'],
            data['rainfall']
        ]])

        # Get top 3 predictions with confidence
        probabilities = crop_model.predict_proba(features)[0]
        top3_indices = np.argsort(probabilities)[::-1][:3]

        top_crops = []
        for idx in top3_indices:
            top_crops.append({
                "name": label_encoder.inverse_transform([idx])[0],
                "confidence": round(float(probabilities[idx]) * 100, 2)
            })

        return jsonify({"top_crops": top_crops}), 200

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400