from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    message = request.json["message"]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
    )

    data = response.json()

    reply = data["choices"][0]["message"]["content"]

    return jsonify({
        "reply": reply
    })

if __name__ == "__main__":
    app.run(debug=True)