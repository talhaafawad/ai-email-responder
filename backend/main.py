from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/generate-reply", methods=["POST"])
def generate_reply():
    data = request.json
    customer_email = data.get("email", "")
    tone = data.get("tone", "friendly")

    prompt = f"""
You are a customer support agent. Respond to the following customer email in a {tone} tone.

Customer Email:
{customer_email}

Reply:
"""

    try:
        response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
)
reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "Backend is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
