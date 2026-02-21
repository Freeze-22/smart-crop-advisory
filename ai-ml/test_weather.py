import requests

response = requests.post(
    'http://127.0.0.1:5001/api/ml/weather-recommend',
    json={
        'lat': 17.3850,
        'lon': 78.4867,
        'n': 50,
        'p': 50,
        'k': 50,
        'ph': 6.5
    }
)

print("Status:", response.status_code)
print("Response:", response.text)
