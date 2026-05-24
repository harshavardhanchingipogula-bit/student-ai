async function sendMessage() {

    const input = document.getElementById("user-input");
    const chatArea = document.getElementById("chat-area");

    const message = input.value.trim();

    if(message === ""){
        return;
    }

    // USER MESSAGE

    const userMessage = document.createElement("div");

    userMessage.classList.add("message");
    userMessage.classList.add("user");

    userMessage.innerText = message;

    chatArea.appendChild(userMessage);

    input.value = "";

    // BOT LOADING MESSAGE

    const botMessage = document.createElement("div");

    botMessage.classList.add("message");
    botMessage.classList.add("bot");

    botMessage.innerText = "Typing...";

    chatArea.appendChild(botMessage);

    chatArea.scrollTop = chatArea.scrollHeight;

    try{

        const response = await fetch("/chat", {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                message:message
            })

        });

        const data = await response.json();

        botMessage.innerText = data.reply;

    }catch(error){

        botMessage.innerText = "Error getting AI response";

    }

    chatArea.scrollTop = chatArea.scrollHeight;
}

/* ENTER KEY */

document
.getElementById("user-input")
.addEventListener("keypress", function(event){

    if(event.key === "Enter"){
        sendMessage();
    }

});