# ElevenLabs + Playwright Voice Automation (method - 3)

This project provides a Python-based automation tool for ElevenLabs using Playwright.
It automates the browser to access Alpha v3 voices using your own ElevenLabs account.

## Supported Voices

Tested voices include:

* Bradford
* Alice
* Aria
* Bill
* Brian
* Callum
* Peter
* Arabella
* Joe Inglewood
* James – Husky & Engaging
* Nichalia Schwartz

> Voice availability depends on your ElevenLabs account access.

## Setup

1. Clone the repository.
2. Install dependencies:

```bash
pip install playwright
playwright install
```

3. Create a `.env` file in the root directory:

```
ELEVENLABS_EMAIL=your_email@example.com  
ELEVENLABS_PASSWORD=your_password
```

## Usage

* On first run, the browser will open (`headless=False`).
* After successful login, your session is saved in the `user_data_dir` directory.
* You can later set `headless=True` to run silently.

## Credit

* [Telegram](https://t.me/david667s)
* Gemini
* GPT
* User-agent spoofing via Playwright

---

If you have any questions, feel free to reach out.

---