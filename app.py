from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin (your GitHub site to talk to this backend)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")  # Pull from Render secrets

@app.route('/')
def home():
    return "Trisha's AI Backend is Running! 💡"


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get("message")
        print("📩 Received Message:", user_msg)

        prompt = f"You are Trisha Bej, an AI assistant representing your portfolio. Respond warmly, smartly, and clearly based on Trisha's skills, projects, and achievements. The user asked: {user_msg}"

       url = f"https://generativelanguage.googleapis.com/v1beta1/models/chat-bison-001:generateMessage?key={GOOGLE_API_KEY}"


        print("🔐 Using API URL:", url)

        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "prompt": {
                    "messages": [{"author": "user", "content": prompt}]
                },
                "temperature": 0.7
            }
        )

        print("📦 API Response Code:", response.status_code)
        print("📨 Raw Response Text:", response.text)

        if response.status_code == 200:
            content = response.json()
            reply = content.get("candidates", [{}])[0].get("content", "Hmm... I couldn't come up with a reply!")
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": "Oops! Google API failed."}), 500

    except Exception as e:
        print("🔥 SERVER ERROR:", e)
        return jsonify({"reply": f"Exception occurred: {str(e)}"}), 500

'''
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get("message")

    prompt = f"You are Trisha Bej, an AI assistant representing your portfolio. Respond warmly, smartly, and clearly based on Trisha's skills, projects, and achievements. The user asked: {user_msg}"

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/chat-bison-001:generateMessage?key={GOOGLE_API_KEY}",
        headers={"Content-Type": "application/json"},
        json={
            "prompt": {
                "messages": [{"author": "user", "content": prompt}]
            },
            "temperature": 0.7
        }
    )

    if response.status_code == 200:
        content = response.json()
        reply = content.get("candidates", [{}])[0].get("content", "Hmm... I couldn't come up with a reply!")
        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": "Oops! Something went wrong on the server side."}), 500
'''
