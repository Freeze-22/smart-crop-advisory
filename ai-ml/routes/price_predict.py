from flask import Blueprint, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

price_bp = Blueprint('price', __name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@price_bp.route('/api/ai/price-predict', methods=['POST'])
def predict_price():
    data = request.get_json()
    crop = data.get('crop')
    season = data.get('season')
    land_area = data.get('land_area')
    soil_type = data.get('soil_type')

    prompt = f"""You are an Indian agricultural market expert.
A farmer wants to grow {crop} in {season} season on {land_area} acres of {soil_type} soil.

Give realistic estimates for Indian market in 2024.
Reply ONLY with this JSON format, no extra text:
{{
  "cost_to_grow": {{
    "seeds": 5000,
    "fertilizer": 3000,
    "irrigation": 2000,
    "labor": 4000,
    "total": 14000
  }},
  "expected_yield_kg": 2000,
  "market_price_per_kg": 25,
  "expected_revenue": 50000,
  "expected_profit": 36000,
  "profit_margin": "72%",
  "tips": "Short tip to maximize profit"
}}
All amounts in Indian Rupees (₹). Scale costs by land area {land_area} acres."""

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
    result = json.loads(clean.strip())
    return jsonify(result)