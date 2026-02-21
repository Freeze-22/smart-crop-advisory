from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.advisory import Advisory

advisory_bp = Blueprint('advisory', __name__)

@advisory_bp.route('/api/advisory', methods=['GET'])
def get_advisory():
    crop = request.args.get('crop')
    season = request.args.get('season')
    soil_type = request.args.get('soil_type')

    query = Advisory.query
    if crop:
        query = query.filter_by(crop=crop)
    if season:
        query = query.filter_by(season=season)
    if soil_type:
        query = query.filter_by(soil_type=soil_type)

    results = query.all()
    return jsonify([a.to_dict() for a in results]), 200

@advisory_bp.route('/api/advisory', methods=['POST'])
@jwt_required()
def create_advisory():
    data = request.get_json()
    advisory = Advisory(
        crop=data['crop'],
        season=data['season'],
        soil_type=data['soil_type'],
        irrigation=data['irrigation'],
        fertilizer=data['fertilizer'],
        pest_control=data['pest_control'],
        n=data['n'],
        p=data['p'],
        k=data['k']
    )
    db.session.add(advisory)
    db.session.commit()
    return jsonify(advisory.to_dict()), 201

@advisory_bp.route('/api/advisory/<int:id>', methods=['PUT'])
@jwt_required()
def update_advisory(id):
    advisory = Advisory.query.get_or_404(id)
    data = request.get_json()
    advisory.crop = data.get('crop', advisory.crop)
    advisory.season = data.get('season', advisory.season)
    advisory.soil_type = data.get('soil_type', advisory.soil_type)
    advisory.irrigation = data.get('irrigation', advisory.irrigation)
    advisory.fertilizer = data.get('fertilizer', advisory.fertilizer)
    advisory.pest_control = data.get('pest_control', advisory.pest_control)
    advisory.n = data.get('n', advisory.n)
    advisory.p = data.get('p', advisory.p)
    advisory.k = data.get('k', advisory.k)
    db.session.commit()
    return jsonify(advisory.to_dict()), 200

@advisory_bp.route('/api/advisory/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_advisory(id):
    advisory = Advisory.query.get_or_404(id)
    db.session.delete(advisory)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 200