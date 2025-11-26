const chatBox = document.getElementById("chatBox");
const input = document.getElementById("userInput");

function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = `message ${sender}`;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function typingAnimation() {
    const div = document.createElement("div");
    div.className = "message bot";
    div.innerText = "Typing...";
    div.id = "typing";
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
    const typingDiv = document.getElementById("typing");
    if (typingDiv) typingDiv.remove();
}

async function sendMsg() {
    let msg = input.value.trim();
    if (!msg) return;

    addMessage(msg, "user");
    input.value = "";
    typingAnimation();

    try {
        const response = await fetch("http://127.0.0.1:8000/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_msg: msg })
        });

        const data = await response.json();
        removeTyping();
        addMessage(data.response || "Error: No response", "bot");

    } catch (err) {
        removeTyping();
        addMessage("Error: " + err.message, "bot");
    }
}

input.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        sendMsg();
    }
});
