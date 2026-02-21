from flask import Blueprint, request, jsonify

pest_bp = Blueprint('pest', __name__)

@pest_bp.route('/api/pest/detect', methods=['POST'])
def detect_pest():
    return jsonify({
        "disease": "Service unavailable on free tier",
        "confidence": 0,
        "message": "Pest detection works locally. Deploy on paid server for full functionality."
    })