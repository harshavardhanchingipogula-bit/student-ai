const sendBtn = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");


// SEND MESSAGE
function sendMessage(){

    let message = userInput.value.trim();

    if(message === ""){
        return;
    }

    // USER MESSAGE
    let userDiv = document.createElement("div");

    userDiv.classList.add("message");
    userDiv.classList.add("user-message");

    userDiv.innerText = message;

    chatBox.appendChild(userDiv);

    // AUTO SCROLL
    chatBox.scrollTop = chatBox.scrollHeight;

    // CLEAR INPUT
    userInput.value = "";



    // BOT THINKING
    setTimeout(() => {

        let botDiv = document.createElement("div");

        botDiv.classList.add("message");
        botDiv.classList.add("bot-message");

        botDiv.innerText = getBotReply(message);

        chatBox.appendChild(botDiv);

        chatBox.scrollTop = chatBox.scrollHeight;

    },1000);

}


// BUTTON CLICK
sendBtn.addEventListener("click", sendMessage);


// ENTER PRESS
userInput.addEventListener("keypress", function(e){

    if(e.key === "Enter"){
        sendMessage();
    }

});



// BOT REPLIES
function getBotReply(message){

    message = message.toLowerCase();


    // GREETINGS
    if(message.includes("hi") || message.includes("hello")){
        return "Hello 👋 How can I help you?";
    }

    // NAME
    else if(message.includes("your name")){
        return "My name is Student AI 🤖";
    }

    // STUDY
    else if(message.includes("study")){
        return "Study daily with consistency 📚";
    }

    // MOTIVATION
    else if(message.includes("motivation")){
        return "Success comes from discipline, not motivation 🔥";
    }

    // MATH
    else if(message.includes("math")){
        return "Practice maths daily to improve fast ➕";
    }

    // PYTHON
    else if(message.includes("python")){
        return "Python is one of the easiest programming languages 🐍";
    }

    // C LANGUAGE
    else if(message.includes("c language")){
        return "C language helps you understand programming fundamentals 💻";
    }

    // AI
    else if(message.includes("ai")){
        return "Artificial Intelligence is the future 🚀";
    }

    // DEFAULT
    else{
        return "I am still learning 🤖";
    }

}