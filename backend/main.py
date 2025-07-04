from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow all origins for testing; tighten this for production

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("OPENAI_API_KEY environment variable not set")

# Initialize OpenAI client with your API key
client = OpenAI(api_key=api_key)

@app.route('/generate-reply', methods=['POST'])
def generate_reply():
    data = request.json
    prompt = data.get("email")

    if not prompt:
        return jsonify({"error": "Missing 'email' in request body"}), 400

    # Create chat completion
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
