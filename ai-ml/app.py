from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["*"])

from routes.chatbot import chatbot_bp
from routes.pest_detect import pest_bp
from routes.ai_advisory import advisory_bp
from routes.price_predict import price_bp
from routes.weather_alert import weather_bp

app.register_blueprint(chatbot_bp)
app.register_blueprint(pest_bp)
app.register_blueprint(advisory_bp)
app.register_blueprint(price_bp)
app.register_blueprint(weather_bp)

@app.route("/")
def home():
    return {"status": "AI/ML server is running!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, host="0.0.0.0", port=port)
