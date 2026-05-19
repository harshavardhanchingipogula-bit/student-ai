let chatCount = 1;

// SEND MESSAGE

async function sendMessage(){

    let input =
    document.getElementById("user-input");

    let message =
    input.value;

    if(message.trim() === ""){
        return;
    }

    let chatContainer =
    document.getElementById("chat-container");

    // USER MESSAGE

    let userDiv =
    document.createElement("div");

    userDiv.className =
    "user-message";

    userDiv.innerText =
    message;

    chatContainer.appendChild(userDiv);

    input.value = "";

    // BOT MESSAGE

    let botDiv =
    document.createElement("div");

    botDiv.className =
    "bot-message";

    botDiv.innerHTML =
    "Typing...";

    chatContainer.appendChild(botDiv);

    autoScroll();

    // FETCH API

    let response =
    await fetch("/chat",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            message:message
        })

    });

    let data =
    await response.json();

    typeEffect(botDiv,data.reply);

    playSound();

    saveHistory(message);

}

// TYPE EFFECT

function typeEffect(element,text){

    element.innerHTML = "";

    let i = 0;

    function typing(){

        if(i < text.length){

            element.innerHTML +=
            text.charAt(i);

            i++;

            autoScroll();

            setTimeout(typing,10);

        }

    }

    typing();

}

// AUTO SCROLL

function autoScroll(){

    let chatContainer =
    document.getElementById("chat-container");

    chatContainer.scrollTop =
    chatContainer.scrollHeight;

}

// ENTER KEY

document.getElementById("user-input")
.addEventListener("keypress",function(event){

    if(event.key === "Enter"){
        sendMessage();
    }

});

// VOICE INPUT

function startVoice(){

    const recognition =
    new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.onresult =
    function(event){

        document.getElementById("user-input").value =
        event.results[0][0].transcript;

    };

    recognition.start();

}

// DARK MODE

function toggleMode(){

    document.body.classList.toggle("light-mode");

}

// NEW CHAT

document.querySelector(".new-chat-btn")
.addEventListener("click",function(){

    document.getElementById("chat-container")
    .innerHTML = `
    <div class="bot-message">
    🤖 Hello! How can I assist you today?
    </div>
    `;

});

// SAVE HISTORY

function saveHistory(message){

    let history =
    document.getElementById("chat-history");

    let item =
    document.createElement("div");

    item.className =
    "history-item";

    item.innerText =
    "Chat " + chatCount;

    chatCount++;

    history.appendChild(item);

}

// FILE UPLOAD

document.getElementById("file-upload")
.addEventListener("change",function(event){

    let file =
    event.target.files[0];

    if(!file){
        return;
    }

    let chatContainer =
    document.getElementById("chat-container");

    // IMAGE

    if(file.type.startsWith("image/")){

        let img =
        document.createElement("img");

        img.className =
        "preview-image";

        img.src =
        URL.createObjectURL(file);

        chatContainer.appendChild(img);

    }

    // PDF

    else if(file.type === "application/pdf"){

        let pdf =
        document.createElement("div");

        pdf.className =
        "bot-message";

        pdf.innerHTML =
        "📄 PDF Uploaded: " + file.name;

        chatContainer.appendChild(pdf);

    }

    // OTHER FILES

    else{

        let fileDiv =
        document.createElement("div");

        fileDiv.className =
        "bot-message";

        fileDiv.innerHTML =
        "📁 File Uploaded: " + file.name;

        chatContainer.appendChild(fileDiv);

    }

    autoScroll();

});

// SOUND

function playSound(){

    let audio =
    new Audio(
    "https://www.soundjay.com/buttons/sounds/button-3.mp3"
    );

    audio.play();

}

// LOAD HISTORY

async function loadHistory(){

    let response =
    await fetch("/history");

    let data =
    await response.json();

    console.log(data);

}

loadHistory();