from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    text = data.get("text", "")
    image = data.get("image")

    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"reply": "Lỗi: Chưa cấu hình GEMINI_API_KEY."}), 500

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": text}]}
        ]
    }

    if image:
        payload["contents"][0]["parts"].append({
            "inline_data": {"mime_type": "image/png", "data": image}
        })

    r = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + api_key,
        headers=headers, json=payload
    )

    if r.status_code != 200:
        return jsonify({"reply": f"Lỗi API ({r.status_code})"}), 500

    data = r.json()
    reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Không có phản hồi.")
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
