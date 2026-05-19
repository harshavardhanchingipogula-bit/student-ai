from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ================= API KEY =================

API_KEY = "YOUR_API_KEY"

# ================= HOME =================

@app.route("/")
def home():
    return render_template("index.html")

# ================= CHATBOT =================

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI Student Assistant."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()

    try:
        reply = result["choices"][0]["message"]["content"]
    except:
        reply = "Error getting response"

    return jsonify({
        "reply": reply
    })

# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)