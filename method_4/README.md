# ElevenLabs TTS V3 (Method 4: Anonymous Landing Stream)

This method uses the new API protocol from the ElevenLabs landing page demo.

## Features
- **Endpoint:** `/v1/text-to-speech/{voice_id}/stream/with-timestamps/anonymous`
- **Model:** `eleven_v3` with full support for emotion tags (`[sarcastically]`, `[whispers]`, `[giggles]`).
- **Languages:** `kk` (Kazakh) and all other supported languages.
- **Data format:** Base64 audio stream delivered in chunks via NDJSON.

## Token is fetched automatically

The script opens elevenlabs.io via **Playwright**, renders the hCaptcha invisible
widget (`sitekey: 8e58fe8c-1a48-4f94-88ae-8e90b586a192`) by itself and grabs the token.
No manual copying from DevTools is needed.

## Usage

```bash
python elevenlabs_tts.py             # opens a browser window (most reliable — usually passes right away)
python elevenlabs_tts.py --headless  # fully automatic; hCaptcha may score it low and return 401
```

> Note: in `headless` mode the hCaptcha token is scored as a "bot",
> so ElevenLabs may respond with `401 detected_unusual_activity`.
> Use the regular (visible) mode instead. If a captcha appears, solve it yourself in the window.

## Requirements

```bash
pip install requests playwright
playwright install chromium
```
