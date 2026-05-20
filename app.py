from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# =========================================
# OPENROUTER API KEY
# =========================================

API_KEY = "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"

# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():
    return render_template("index.html")

# =========================================
# CHAT API
# =========================================

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-chat",

        "messages": [
            {
                "role": "system",
                "content": "You are Student AI, a helpful study assistant."
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

        return jsonify({
            "reply": f"Error: {str(e)}"
        })

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":
    app.run(debug=True)