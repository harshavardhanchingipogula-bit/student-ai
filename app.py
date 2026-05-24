from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# API KEY FROM RENDER ENVIRONMENT VARIABLE
API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://student-ai-3.onrender.com",
        "X-Title": "Student AI",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()

        print(result)

        reply = result["choices"][0]["message"]["content"]

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print(e)

        return jsonify({
            "reply": "Error getting AI response"
        })

if __name__ == "__main__":
    app.run(debug=True)