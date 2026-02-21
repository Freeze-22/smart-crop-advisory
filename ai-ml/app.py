from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

from routes.chatbot import chatbot_bp
from routes.pest_detect import pest_bp
from routes.ai_advisory import advisory_bp

app.register_blueprint(chatbot_bp)
app.register_blueprint(pest_bp)
app.register_blueprint(advisory_bp)

@app.route("/")
def home():
    return {"status": "AI/ML server is running!"}

if __name__ == "__main__":
    app.run(debug=True, port=5001)
