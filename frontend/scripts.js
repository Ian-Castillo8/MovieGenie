const API_URL = "http://4.149.91.202:5000/chat";

async function answer(val) {
    const userAnswer = val === 1 ? "yes" : "no";

    const reply = await sendToAPI(userAnswer);

    document.getElementById("question").innerText = reply;

    if (reply.toLowerCase().includes("i think your movie is")) {
        showResult(reply);
    }
}

async function sendToAPI(message) {
    const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await res.json();
    return data.reply;
}

function showResult(text) {
    document.getElementById("game-box").style.display = "none";
    document.getElementById("result-box").style.display = "block";
    document.getElementById("result").innerText = text;
}
