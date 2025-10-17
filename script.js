document.getElementById("sendBtn").addEventListener("click", sendMessage);

async function sendMessage() {
  const input = document.getElementById("userInput");
  const chatbox = document.getElementById("chatbox");

  const userMessage = input.value.trim();
  if (!userMessage) return;

  chatbox.innerHTML += `<div class="message user"><b>Bạn:</b> ${userMessage}</div>`;
  input.value = "";

  chatbox.innerHTML += `<div class="message bot"><i>Đang trả lời...</i></div>`;
  chatbox.scrollTop = chatbox.scrollHeight;

  try {
    const res = await fetch("/api/gemini", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: userMessage })
    });

    const data = await res.json();
    const botReply = data.reply || "Lỗi: Không có phản hồi.";

    chatbox.lastElementChild.innerHTML = `<b>Gemini:</b> ${botReply}`;
    chatbox.scrollTop = chatbox.scrollHeight;
  } catch (error) {
    chatbox.lastElementChild.innerHTML = `<b>Lỗi:</b> ${error.message}`;
  }
}
