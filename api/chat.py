from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.post("/api/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": user_message}]}]}

    response = requests.post(f"{url}?key={GEMINI_API_KEY}", headers=headers, json=payload)
    result = response.json()

    ai_text = result["candidates"][0]["content"]["parts"][0]["text"]
    return JSONResponse({"reply": ai_text})
