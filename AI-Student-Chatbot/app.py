from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ======================================
# OPENROUTER API KEY
# ======================================

API_KEY = "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"

# ======================================
# HOME PAGE
# ======================================

@app.route("/")

def home():

    return render_template("index.html")

# ======================================
# CHAT API
# ======================================

@app.route("/chat", methods=["POST"])

def chat():

    data = request.get_json()

    user_message = data["message"]

    headers = {

        "Authorization":
        f"Bearer {API_KEY}",

        "Content-Type":
        "application/json"

    }

    payload = {

        "model":
        "openai/gpt-3.5-turbo",

        "messages":[

            {
                "role":"system",

                "content":
                "You are a helpful AI student assistant."
            },

            {
                "role":"user",

                "content":
                user_message
            }

        ]

    }

    response = requests.post(

        "https://openrouter.ai/api/v1/chat/completions",

        headers=headers,

        json=payload

    )

    result = response.json()

    try:

        reply = result["choices"][0]["message"]["content"]

    except:

        reply = "Error getting AI response"

    return jsonify({

        "reply": reply

    })

# ======================================
# RUN APP
# ======================================

if __name__ == "__main__":

    app.run(debug=True)