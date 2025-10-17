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
        return jsonify({"reply": "❌ Chưa cấu hình GEMINI_API_KEY"}), 500

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": text}]
                + ([{"inline_data": {"mime_type": "image/png", "data": image}}] if image else [])
            }
        ]
    }

    # ✅ Endpoint CHUẨN NHẤT (2025)
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"

    try:
        r = requests.post(url, headers=headers, json=payload)
        if r.status_code != 200:
            return jsonify({"reply": f"Lỗi API ({r.status_code}): {r.text}"}), 500

        res = r.json()
        reply = (
            res.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "Không có phản hồi từ AI.")
        )
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Lỗi hệ thống: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
