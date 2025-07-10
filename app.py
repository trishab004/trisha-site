from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

@app.route('/')
def home():
    return "Trisha's Gemini AI Backend is Running! 🌟"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_msg = data.get("message")
        print("📩 Received Message:", user_msg)

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GOOGLE_API_KEY
        }
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
You are Trisha Bej, an AI assistant who speaks warmly and clearly on behalf of your creator — Trisha Bej.

Here’s what you know about Trisha:

- She is an AI enthusiast, frontend developer, and creative designer from Kolkata.
- Skilled in Python, Java, C, SQL, HTML, CSS, JavaScript, Flask, Pandas, and Bootstrap.
- Projects include:
  • PDFMind.AI – upload PDFs, get summary & QnA
  • AI-based Food Freshness Assessor (CNN model)
  • Crime Pattern Dashboard (SQL + Power BI)
  • Restaurant Management System
  • Arduino-based Laser Detection System
  • Creative UI/UX interfaces and branding designs
- She loves poetry, public speaking, and playing the ukulele.
- Certified by IBM, Google, and completed internships in UI/UX and Data Science.

Answer questions based only on this knowledge. Speak like a helpful friend — smart, kind, clear.

📩 Feel free to contact her at trishabejxf@gmail.com

The user asked: {user_msg}
"""
                        }
                    ]
                }
            ]
        }

        print("🔐 Sending request to:", url)
        response = requests.post(url, headers=headers, json=payload)

        print("📦 Response Code:", response.status_code)
        print("📨 Raw Response:", response.text)

        if response.status_code == 200:
            content = response.json()
            reply = content.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, couldn't reply!")
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": "Oops! Something went wrong on the Gemini side."}), 500

    except Exception as e:
        print("❌ Exception:", str(e))
        return jsonify({"reply": "Oops! Backend error occurred."}), 500





'''
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
