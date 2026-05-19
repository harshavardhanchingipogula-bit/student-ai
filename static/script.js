async function sendMessage() {

    let input = document.getElementById("user-input");

    let message = input.value;

    if(message.trim() === ""){
        return;
    }

    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

    input.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;

    document.getElementById("typing").classList.remove("hidden");


    let response = await fetch("/chat", {

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            message:message
        })

    });


    let data = await response.json();

    document.getElementById("typing").classList.add("hidden");


    chatBox.innerHTML += `
        <div class="bot-message">
            ${data.reply}
        </div>
    `;


    chatBox.scrollTop = chatBox.scrollHeight;
}


function handleEnter(event){

    if(event.key === "Enter"){
        sendMessage();
    }

}


function startVoice(){

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.onresult = function(event){

        document.getElementById("user-input").value = event.results[0][0].transcript;

    };

    recognition.start();
}