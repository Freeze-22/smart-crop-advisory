from flask import Blueprint, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

calculator_bp = Blueprint('calculator', __name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@calculator_bp.route('/api/calculator/pesticide', methods=['POST'])
def pesticide_calculator():
    data = request.get_json()
    crop = data.get('crop')
    land_area = data.get('land_area')
    pest_type = data.get('pest_type')
    severity = data.get('severity', 'medium')

    prompt = f"""You are an Indian agricultural expert.
Calculate pesticide requirement for:
Crop: {crop}, Land: {land_area} acres, Pest: {pest_type}, Severity: {severity}

Reply ONLY with this JSON, no extra text:
{{
  "pesticide_name": "name",
  "quantity_needed": "X liters/kg",
  "dilution_ratio": "1:X with water",
  "application_method": "spray/soil",
  "frequency": "X times per week",
  "cost_estimate": "₹XXXX",
  "safety_tips": "important safety tip",
  "organic_alternative": "organic option"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
    clean = reply.strip()
    if '```' in clean:
        clean = clean.split('```')[1]
        if clean.startswith('json'):
            clean = clean[4:]
    return jsonify(json.loads(clean.strip()))

@calculator_bp.route('/api/calculator/fertilizer', methods=['POST'])
def fertilizer_calculator():
    data = request.get_json()
    crop = data.get('crop')
    land_area = data.get('land_area')
    soil_type = data.get('soil_type')
    growth_stage = data.get('growth_stage', 'sowing')

    prompt = f"""You are an Indian agricultural expert.
Calculate fertilizer requirement for:
Crop: {crop}, Land: {land_area} acres, Soil: {soil_type}, Stage: {growth_stage}

Reply ONLY with this JSON, no extra text:
{{
  "npk_ratio": "N:P:K ratio",
  "urea_kg": 50,
  "dap_kg": 30,
  "mop_kg": 20,
  "micronutrients": "zinc/boron etc",
  "application_schedule": "when to apply",
  "total_cost": "₹XXXX",
  "tips": "important tip for best yield"
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
    clean = reply.strip()
    if '```' in clean:
        clean = clean.split('```')[1]
        if clean.startswith('json'):
            clean = clean[4:]
    return jsonify(json.loads(clean.strip()))