# ElevenLabs + Playwright Voice Automation

This project provides a Python non-official API for ElevenLabs using Playwright automation. Supported Alpha v3 model voices.

## Available Voices

The following voices are supported:

1. Bradford
2. Alice
3. Alice
4. Aria
5. Bill
6. Brian
7. Callum
8. Peter
9. Arabella
10. Joe Inglewood
11. Bradford
12. James - Husky & Engaging
13. Nichalia Schwartz

## Setup

1. Clone this repository.
2. Install Playwright:

```
pip install playwright
playwright install
```
3. Create a `.env` file in the project root with your ElevenLabs account credentials:

```
ELEVENLABS_EMAIL=your_email@example.com
ELEVENLABS_PASSWORD=your_password
```

## Usage

On first run, the browser opens because `headless=False` is set in the code. Later, you can set `headless=True` to run without opening a browser window.

The `user_data_dir` directory is used to store your browser session and authentication data, so you don't need to log in every time.

## Note

This repository contains two separate methods for working with ElevenLabs:

- `method_1/` — contains the first approach (see `elevenlabs_client.py`, `example.py`).
- `method_2/` — contains the second approach (see `elevenlabs_tts.py`).

Choose the method that best fits your needs.

---

## Credit

- [t.me/david667s](https://t.me/david667s)
- Gemini
- GPT
- browser-use agent

If you have any questions, feel free to ask!
