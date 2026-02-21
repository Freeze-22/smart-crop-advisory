from flask import Blueprint, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import requests
import os

load_dotenv()

weather_bp = Blueprint('weather', __name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@weather_bp.route('/api/weather/alert', methods=['GET'])
def weather_alert():
    lat = request.args.get('lat', '20.5937')
    lon = request.args.get('lon', '78.9629')

    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,windspeed_10m&daily=precipitation_sum,temperature_2m_max,temperature_2m_min&forecast_days=3"
    
    weather_res = requests.get(weather_url)
    weather_data = weather_res.json()

    current = weather_data['current']
    temp = current['temperature_2m']
    humidity = current['relative_humidity_2m']
    precipitation = current['precipitation']
    windspeed = current['windspeed_10m']

    prompt = f"""You are an Indian agricultural weather expert.
Current weather: Temperature={temp}°C, Humidity={humidity}%, Precipitation={precipitation}mm, Wind={windspeed}km/h

Reply ONLY with this JSON, no extra text:
{{
  "alert_level": "low/medium/high",
  "alert_message": "Short weather alert for farmers",
  "crop_advice": "What farmers should do now",
  "seasonal_crops": ["crop1", "crop2", "crop3"]
}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    import json
    reply = response.choices[0].message.content
    clean = reply.strip()
    if '```' in clean:
        clean = clean.split('```')[1]
        if clean.startswith('json'):
            clean = clean[4:]
    
    result = json.loads(clean.strip())
    result['temperature'] = temp
    result['humidity'] = humidity
    result['precipitation'] = precipitation
    
    return jsonify(result)