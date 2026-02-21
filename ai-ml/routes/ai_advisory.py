from flask import Blueprint, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

advisory_bp = Blueprint('advisory', __name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@advisory_bp.route('/api/ai/generate-advisory', methods=['POST'])
def generate_advisory():
    data = request.get_json()
    crop = data.get('crop')
    season = data.get('season')
    soil_type = data.get('soil_type')

    prompt = f"""Generate a crop advisory for:
Crop: {crop}, Season: {season}, Soil Type: {soil_type}

Reply ONLY with a JSON object in this exact format:
{{
  "irrigation": "irrigation advice here",
  "fertilizer": "fertilizer advice here",
  "pest_control": "pest control advice here",
  "n": 90,
  "p": 40,
  "k": 40
}}
No extra text, just the JSON."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response.choices[0].message.content
    advisory = json.loads(reply)
    advisory['crop'] = crop
    advisory['season'] = season
    advisory['soil_type'] = soil_type

    return jsonify(advisory)