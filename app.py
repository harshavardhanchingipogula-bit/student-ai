from flask import Flask, request, jsonify
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

    return """

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Student AI</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial,sans-serif;
}

body{
    background:#020f2f;
    color:white;
    height:100vh;
    overflow:hidden;
}

.container{
    display:flex;
    height:100vh;
}

.sidebar{
    width:220px;
    background:#08163f;
    padding:20px;
}

.logo{
    font-size:32px;
    font-weight:bold;
    margin-bottom:25px;
}

.new-chat{
    width:100%;
    padding:14px;
    border:none;
    border-radius:14px;
    background:#2563eb;
    color:white;
    font-size:16px;
    cursor:pointer;
}

.main{
    flex:1;
    display:flex;
    flex-direction:column;
}

.header{
    padding:20px;
    border-bottom:1px solid rgba(255,255,255,0.1);
}

.title{
    font-size:55px;
    font-weight:bold;
}

.subtitle{
    margin-top:8px;
    color:#bcd0ff;
}

.chat-box{
    flex:1;
    overflow-y:auto;
    padding:20px;
    display:flex;
    flex-direction:column;
    gap:20px;
    padding-bottom:120px;
}

.message{
    max-width:75%;
    padding:16px;
    border-radius:18px;
    line-height:1.6;
    font-size:16px;
    white-space:pre-wrap;
}

.user{
    background:#2563eb;
    margin-left:auto;
}

.bot{
    background:#142552;
}

.input-area{
    position:fixed;
    bottom:0;
    left:220px;
    right:0;
    background:#08163f;
    padding:12px;
    display:flex;
    gap:10px;
}

#message{
    flex:1;
    padding:16px;
    border:none;
    border-radius:14px;
    background:#13265b;
    color:white;
    font-size:16px;
    outline:none;
}

button{
    border:none;
    border-radius:14px;
    cursor:pointer;
}

#send-btn{
    width:70px;
    background:#2563eb;
    color:white;
    font-size:18px;
}

#voice-btn{
    width:60px;
    background:#142552;
    color:white;
    font-size:20px;
}

.typing{
    opacity:0.7;
    animation:blink 1s infinite;
}

@keyframes blink{

    0%{
        opacity:0.4;
    }

    50%{
        opacity:1;
    }

    100%{
        opacity:0.4;
    }

}

@media(max-width:768px){

    .sidebar{
        display:none;
    }

    .input-area{
        left:0;
    }

    .title{
        font-size:34px;
    }

    .message{
        max-width:90%;
    }

}

</style>

</head>

<body>

<div class="container">

<div class="sidebar">

<div class="logo">
🎓 Student AI
</div>

<button class="new-chat">
+ New Chat
</button>

</div>

<div class="main">

<div class="header">

<div class="title">
AI Student Chatbot
</div>

<div class="subtitle">
Your Personal AI Study Assistant
</div>

</div>

<div class="chat-box" id="chat-box">

<div class="message bot">
🤖 Hello! Ask me anything.
</div>

</div>

<div class="input-area">

<button id="voice-btn">
🎤
</button>

<input
type="text"
id="message"
placeholder="Ask anything...">

<button id="send-btn">
➤
</button>

</div>

</div>

</div>

<script>

const sendBtn =
document.getElementById("send-btn");

const input =
document.getElementById("message");

const chatBox =
document.getElementById("chat-box");

function addMessage(text,type){

    const div =
    document.createElement("div");

    div.classList.add(
        "message",
        type
    );

    div.innerText = text;

    chatBox.appendChild(div);

    chatBox.scrollTop =
    chatBox.scrollHeight;
}

async function sendMessage(){

    let msg =
    input.value.trim();

    if(msg === ""){
        return;
    }

    addMessage(msg,"user");

    input.value = "";

    const typing =
    document.createElement("div");

    typing.classList.add(
        "message",
        "bot",
        "typing"
    );

    typing.innerText =
    "Typing...";

    chatBox.appendChild(typing);

    chatBox.scrollTop =
    chatBox.scrollHeight;

    try{

        const response =
        await fetch("/chat",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:msg
            })

        });

        const data =
        await response.json();

        typing.remove();

        addMessage(data.reply,"bot");

    }

    catch(error){

        typing.remove();

        addMessage(
            "AI connection error",
            "bot"
        );

    }

}

sendBtn.addEventListener(
"click",
sendMessage
);

input.addEventListener(
"keypress",

function(e){

    if(e.key === "Enter"){

        sendMessage();

    }

});

const SpeechRecognition =
window.SpeechRecognition ||
window.webkitSpeechRecognition;

if(SpeechRecognition){

    const recognition =
    new SpeechRecognition();

    recognition.lang =
    "en-US";

    document
    .getElementById("voice-btn")
    .addEventListener("click",()=>{

        recognition.start();

    });

    recognition.onresult =
    function(event){

        input.value =
        event.results[0][0].transcript;

        sendMessage();

    };

}

</script>

</body>

</html>

"""

# =========================================
# CHAT API
# =========================================

@app.route("/chat", methods=["POST"])

def chat():

    try:

        data = request.get_json()

        user_message = data["message"]

        headers = {

            "Authorization":
            f"Bearer {API_KEY}",

            "HTTP-Referer":
            "http://localhost:5000",

            "X-Title":
            "Student AI",

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
                    "You are a helpful AI assistant."
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

        print(result)

        if "choices" in result:

            reply = result["choices"][0]["message"]["content"]

        else:

            reply = str(result)

        return jsonify({

            "reply": reply

        })

    except Exception as e:

        return jsonify({

            "reply": str(e)

        })

# =========================================
# RUN APP
# =========================================

if __name__ == "__main__":

    app.run(debug=True)