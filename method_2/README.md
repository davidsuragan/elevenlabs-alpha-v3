# ElevenLabs TTS V3 (method 2)

This script demonstrates a simple way to send a POST request to the ElevenLabs API for text-to-speech synthesis. 

- This script uses the free demo version of the elevenlabs.io
- ElevenLabs provides limited access to its API for testing and non-commercial use without requiring an API key.
- You can try the demo without registration, but expect possible rate limits and temporary restrictions.
- You cab set many voice_id!


## Usage

- Edit the script to set your desired text and select a voice ID.
- Run the script:
  ```
  python elevenlabs_tts.py
  ```
- The resulting audio will be saved as `output.mp3` if the request is successful.

## Notes & Limitations

- This script uses the public ElevenLabs API endpoint and does not require authentication.
- There are rate limits and restrictions: after several requests, the API may stop working or block further requests.
- If you encounter issues (e.g., errors, no audio), try using a VPN or proxy to bypass possible IP-based restrictions.
- For more robust and reliable usage, consider using an official API key and following ElevenLabs' official documentation.

---

## Credit

- [t.me/david667s](https://t.me/david667s)
- Gemini
- GPT