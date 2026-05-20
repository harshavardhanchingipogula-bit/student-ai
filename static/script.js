const sendBtn = document.getElementById("send-btn");

const userInput = document.getElementById("user-input");

const chatBox = document.getElementById("chat-box");

async function sendMessage() {

    const message = userInput.value;

    if(message.trim() === ""){
        return;
    }

    // USER MESSAGE

    const userMessage = document.createElement("div");

    userMessage.classList.add("message", "user");

    userMessage.innerText = message;

    chatBox.appendChild(userMessage);

    userInput.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;

    try{

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        // AI MESSAGE

        const aiMessage = document.createElement("div");

        aiMessage.classList.add("message", "ai");

        aiMessage.innerText = data.reply;

        chatBox.appendChild(aiMessage);

        chatBox.scrollTop = chatBox.scrollHeight;

    }

    catch(error){

        const aiMessage = document.createElement("div");

        aiMessage.classList.add("message", "ai");

        aiMessage.innerText = "Error connecting to AI.";

        chatBox.appendChild(aiMessage);
    }
}

// SEND BUTTON

sendBtn.addEventListener("click", sendMessage);

// ENTER BUTTON

userInput.addEventListener("keypress", function(e){

    if(e.key === "Enter"){

        sendMessage();
    }
});

// =========================================
// VOICE INPUT
// =========================================

const voiceBtn = document.getElementById("voice-btn");

const SpeechRecognition =
window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();

recognition.lang = "en-US";

voiceBtn.addEventListener("click", () => {

    recognition.start();

});

recognition.onresult = function(event){

    const transcript = event.results[0][0].transcript;

    userInput.value = transcript;

    sendMessage();
};