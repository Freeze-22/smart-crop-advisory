from flask import Blueprint, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are AgriBot, an expert assistant for Indian farmers. 
Give practical advice on crops, irrigation, pest control, and fertilizers. 
Be concise and helpful. Answer in simple English."""

@chatbot_bp.route('/api/ai/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    history = data.get('history', [])

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    for h in history:
        messages.append(h)
    
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})