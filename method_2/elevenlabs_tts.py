import requests

# Voice IDs
LIAM = "cgSgspJ2msm6clMCkdW9"
JESSICA = "TX3LPaxmHKxFdv7VOQHJ"
ANNOUNCER = "gU0LNdkMOQCOrPrwtbee"
SAMMARA = "19STyYD15bswVz51nqLf"
SERGEANT = "DGzg6RaUqxGRTHSBjfgF"
SPUDS = "NOpBlnGInO9m6vDvFkFC"

# Text to synthesize
text = "[sympathetic] Сәлеметсіз бе. Жесика байланыста. [professional] Сізге қалай көмектесе аламын?"
voice_id = JESSICA  # Change to any of the above

url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream?allow_unauthenticated=1"
payload = {
    "text": text,
    "model_id": "eleven_v3",
    "voice_settings": {
        "speed": 1
    }
}
headers = {
    "accept": "audio/mpeg",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    with open("output.mp3", "wb") as f:
        f.write(response.content)
    print("Audio saved as output.mp3")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
