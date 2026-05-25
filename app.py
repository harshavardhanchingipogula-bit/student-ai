from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"

@app.route("/")
def home():

    return render_template("index.html")

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

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=True
    )