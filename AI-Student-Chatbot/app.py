from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.secret_key = "studentai"

# DATABASE

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# USER TABLE

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(100))

# CHAT TABLE

class Chat(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    user_message = db.Column(db.Text)

    bot_reply = db.Column(db.Text)

# CREATE DATABASE

with app.app_context():
    db.create_all()

# OPENROUTER API

API_KEY = "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"

# HOME

@app.route("/")

def home():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "index.html",
        username=session["user"]
    )

# SIGNUP

@app.route("/signup", methods=["GET", "POST"])

def signup():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:
            return "User already exists"

        new_user = User(
            username=username,
            password=password
        )

        db.session.add(new_user)

        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")

# LOGIN

@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username,
            password=password
        ).first()

        if user:

            session["user"] = username

            return redirect("/")

        else:
            return "Invalid username or password"

    return render_template("login.html")

# LOGOUT

@app.route("/logout")

def logout():

    session.pop("user", None)

    return redirect("/login")

# CHAT API

@app.route("/chat", methods=["POST"])

def chat():

    try:

        data = request.get_json()

        user_message = data["message"]

        headers = {

            "Authorization": f"Bearer {API_KEY}",

            "Content-Type": "application/json"

        }

        payload = {

            "model": "openai/gpt-3.5-turbo",

            "messages": [

                {
                    "role": "system",

                    "content": "You are a helpful AI study assistant."
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

            json=payload

        )

        result = response.json()

        print(result)

        bot_reply = result["choices"][0]["message"]["content"]

        # SAVE CHAT

        if "user" in session:

            new_chat = Chat(

                username=session["user"],

                user_message=user_message,

                bot_reply=bot_reply

            )

            db.session.add(new_chat)

            db.session.commit()

        return jsonify({

            "reply": bot_reply

        })

    except Exception as e:

        return jsonify({

            "reply": str(e)

        })

# CHAT HISTORY

@app.route("/history")

def history():

    if "user" not in session:
        return redirect("/login")

    chats = Chat.query.filter_by(
        username=session["user"]
    ).all()

    data = []

    for chat in chats:

        data.append({

            "user_message": chat.user_message,

            "bot_reply": chat.bot_reply

        })

    return jsonify(data)

# DELETE CHAT

@app.route("/delete_chat", methods=["POST"])

def delete_chat():

    if "user" not in session:
        return jsonify({"status":"error"})

    Chat.query.filter_by(
        username=session["user"]
    ).delete()

    db.session.commit()

    return jsonify({

        "status":"success"

    })

# RUN

if __name__ == "__main__":

    app.run(debug=True)