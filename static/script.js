async function sendMessage(){

    const input = document.getElementById("user-input");

    const chatArea = document.getElementById("chat-area");

    const message = input.value;

    if(message == ""){
        return;
    }

    const userDiv = document.createElement("div");

    userDiv.className = "message user";

    userDiv.innerText = message;

    chatArea.appendChild(userDiv);

    input.value = "";

    const botDiv = document.createElement("div");

    botDiv.className = "message bot";

    botDiv.innerText = "Typing...";

    chatArea.appendChild(botDiv);

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

    botDiv.innerText = data.reply;

    chatArea.scrollTop = chatArea.scrollHeight;
}