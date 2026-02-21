from flask import Blueprint, request, jsonify
import requests

weather_crop_bp = Blueprint('weather_crop', __name__)

@weather_crop_bp.route('/api/ml/weather-recommend', methods=['POST'])
def weather_recommend():
    data = request.get_json()
    lat = data.get('lat', 20.5937)  # Default: India center
    lon = data.get('lon', 78.9629)
    n = data.get('n', 50)
    p = data.get('p', 50)
    k = data.get('k', 50)
    ph = data.get('ph', 6.5)

    # Fetch live weather from Open-Meteo
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,rain"
    weather_res = requests.get(weather_url).json()

    current = weather_res['current']
    temperature = current['temperature_2m']
    humidity = current['relative_humidity_2m']
    rainfall = current['rain']

    # Call Laptop 1's ML route
    ml_url = "http://10.250.29.123:5000/api/ml/recommend-crop"
    ml_res = requests.post(ml_url, json={
        "n": n, "p": p, "k": k,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }).json()

    return jsonify({
        "weather": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        },
        "recommended_crops": ml_res.get('top_crops', [])
    })