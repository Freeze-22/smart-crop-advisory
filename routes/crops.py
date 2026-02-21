from flask import Blueprint, jsonify
from models.advisory import Advisory

crops_bp = Blueprint('crops', __name__)

@crops_bp.route('/api/crops', methods=['GET'])
def get_crops():
    crops = Advisory.query.with_entities(Advisory.crop).distinct().all()
    crop_list = [c[0] for c in crops]
    return jsonify(crop_list), 200