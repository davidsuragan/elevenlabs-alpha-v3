import requests
import json

# Voice IDs
JESSICA = "cgSgspJ2msm6clMCkdW9"

# LIAM = "TX3LPaxmHKxFdv7VOQHJ"
# ANNOUNCER = "gU0LNdkMOQCOrPrwtbee"
# SAMMARA = "19STyYD15bswVz51nqLf"
# SERGEANT = "DGzg6RaUqxGRTHSBjfgF"
# SPUDS = "NOpBlnGInO9m6vDvFkFC"
# your_voice_id = "This is Insane Bro!"

# Text to synthesize

text = f"[sympathetic] Hello. I am Jessica, and [professional] I support the ElevenLabs V3 text-to-speech model. How may I assist you today?"
voice_id = JESSICA

# URL for unauthenticated access
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream?allow_unauthenticated=1"

# The data to be sent to the API
payload = {
    "text": text,
    "model_id": "eleven_v3",
    "voice_settings": {
        "speed": 1
    }
}

# Headers to mimic a browser request
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "Origin": "https://elevenlabs.io",
    "Referer": "https://elevenlabs.io/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

try:
    # Sending the POST request
    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        print("Audio saved successfully: output.mp3")
    else:
        # Print error details if the request failed
        print(f"Error: {response.status_code}")
        try:
            print(response.json())
        except json.JSONDecodeError:
            print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")