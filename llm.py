import requests
from config import GEMINI_API_KEY

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta"

def get_embedding(text):
    url = f"{GEMINI_URL}/models/embedding-001:embedContent?key={GEMINI_API_KEY}"
    data = {
        "model": "models/embedding-001",
        "content": {
            "parts": [{"text": text}]
        }
    }
    r = requests.post(url, json=data)
    r.raise_for_status()
    return r.json()["embedding"]["values"]

def ask_gemini(prompt):
    url = f"{GEMINI_URL}/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(url, json=data)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"]
