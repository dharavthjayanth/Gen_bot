const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const clearBtn = document.getElementById("clear-btn");
const loading = document.getElementById("loading");

function addMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, "user");
    userInput.value = "";
    loading.classList.remove("hidden");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        loading.classList.add("hidden");

        if (data.reply) {
            addMessage(data.reply, "bot");
        } else {
            addMessage(data.error || "Something went wrong.", "bot");
        }
    } catch (error) {
        loading.classList.add("hidden");
        addMessage("Server error. Please try again.", "bot");
    }
}

async function clearChat() {
    await fetch("/clear", { method: "POST" });
    chatBox.innerHTML = "";
}

sendBtn.addEventListener("click", sendMessage);
clearBtn.addEventListener("click", clearChat);

userInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});