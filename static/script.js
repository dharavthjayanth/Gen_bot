async function sendMessage() {
    let input = document.getElementById("message");
    let message = input.value.trim();

    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    document.getElementById("loading").style.display = "block";

    let response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message})
    });

    let data = await response.json();

    document.getElementById("loading").style.display = "none";

    if (data.reply) {
        addMessage(data.reply, "bot");
    } else {
        addMessage("Error: " + data.error, "bot");
    }
}

function addMessage(text, sender) {
    let chat = document.getElementById("chat-box");

    let div = document.createElement("div");
    div.className = sender;
    div.innerText = text;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function clearChat() {
    await fetch("/clear", {method: "POST"});
    document.getElementById("chat-box").innerHTML = "";
}

document.getElementById("message").addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});