import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("ELEVENLABS_EMAIL")
PASSWORD = os.getenv("ELEVENLABS_PASSWORD")
API_KEY = os.getenv("FIREBASE_API_KEY")

voice_id = "cgSgspJ2msm6clMCkdW9"  # Set your desired voice ID here

url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

headers = {
    "Referer": "https://elevenlabs.io",
    "Origin": "https://elevenlabs.io",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

payload = {
    "email": EMAIL,
    "password": PASSWORD,
    "returnSecureToken": True
}

token = None
try:
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        token = r.json()['idToken']
        print("✅ Token OK")
    else:
        print(f"❌ Firebase error [{r.status_code}]: {r.text}")
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")

if token:
    url = "https://api.us.elevenlabs.io/v1/text-to-dialogue/stream"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "Origin": "https://elevenlabs.io",
        "Referer": "https://elevenlabs.io/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "authorization": f"Bearer {token}"
    }
    payload = {
        "inputs": [
            {
                "text": "Great, this method worked! Everything is clear now.",
                "voice_id": voice_id
            }
        ],
        "model_id": "eleven_v3",
        "settings": {
            "stability": 0.5,
            "use_speaker_boost": True
        }
    }
    print("🔊 Sending request to ElevenLabs...")
    r = requests.post(url, json=payload, headers=headers, stream=True)
    if r.status_code == 200:
        with open("final_output.mp3", "wb") as f:
            for chunk in r.iter_content(4096):
                f.write(chunk)
        print("✅ Audio saved: final_output.mp3")
    else:
        print(f"❌ ElevenLabs error [{r.status_code}]:")
        try:
            print(r.json())
        except json.JSONDecodeError:
            print(r.text)
