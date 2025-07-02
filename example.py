from elevenlabs_client import ElevenLabsClient
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv('ELEVENLABS_EMAIL')
PASSWORD = os.getenv('ELEVENLABS_PASSWORD')

voice_name = "Bradford"  # Set your desired voice name here
headless=False  # Set to True if you want to run in headless mode

with ElevenLabsClient(email=EMAIL, password=PASSWORD) as client:
    client.launch(headless=headless)
    client.generate_and_download(
        voice_name=voice_name,
        text="Welcome to ElevenLabs non official API. By David Suragan!"
    )
    # 2 audio files will be generated.