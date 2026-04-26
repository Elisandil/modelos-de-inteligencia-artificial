INDEX_HTML = """<!DOCTYPE html>
<html>
<head>
  <title>Chatbot</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 0 20px; }
    h2 { color: #333; }
    #chat { border: 1px solid #ccc; border-radius: 8px; padding: 10px; height: 350px; overflow-y: auto; margin-bottom: 10px; background: #f9f9f9; }
    #chat p { margin: 6px 0; }
    .user { color: #0066cc; }
    .bot { color: #228B22; }
    #input-area { display: flex; gap: 8px; }
    #msg { flex: 1; padding: 8px; border: 1px solid #ccc; border-radius: 6px; font-size: 14px; }
    button { padding: 8px 16px; background: #0066cc; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }
    button:hover { background: #0052a3; }
  </style>
</head>
<body>
  <h2>Chatbot</h2>
  <div id="chat"></div>
  <div id="input-area">
    <input id="msg" type="text" placeholder="Type a message...">
    <button id="send-btn">Send</button>
  </div>
  <script>
    const chat = document.getElementById("chat");
    const input = document.getElementById("msg");

    async function send() {
      const text = input.value.trim();
      if (!text) return;
      chat.insertAdjacentHTML("beforeend", `<p class="user"><b>You:</b> ${text}</p>`);
      input.value = "";
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });
      const { response } = await res.json();
      chat.insertAdjacentHTML("beforeend", `<p class="bot"><b>Bot:</b> ${response}</p>`);
      chat.scrollTop = chat.scrollHeight;
    }

    document.getElementById("send-btn").addEventListener("click", send);
    input.addEventListener("keypress", e => { if (e.key === "Enter") send(); });
  </script>
</body>
</html>"""