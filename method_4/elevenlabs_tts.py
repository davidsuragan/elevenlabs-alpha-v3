import base64
import json
import sys
import time
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

VOICE_ID = "cgSgspJ2msm6clMCkdW9"
TTS_URL = (
    f"https://api.elevenlabs.io/v1/text-to-speech/"
    f"{VOICE_ID}/stream/with-timestamps/anonymous"
)
OUTPUT_FILE = Path("output_v3_kk.mp3")

SITE_URL = "https://elevenlabs.io"
HCAPTCHA_SITEKEY = "8e58fe8c-1a48-4f94-88ae-8e90b586a192"
TOKEN_TIMEOUT_S = 180

TEXT = (
    "Елдорияның ежелгі елінде, аспаны жарқырап, ормандары желге "
    "құпияларын сыбырлаған жерде, Зефирос атты айдаһар өмір сүрді. "
    "Ол бәрін өртеп жіберетін түрі емес, бірақ жұмсақ әрі дана айдаһар еді."
)

SETUP_CAPTCHA_JS = """
() => {
    window.__capToken = null;
    window.__capError = null;
    window.__capChallengeOpen = false;

    const container = document.createElement('div');
    container.id = '__anon_captcha';
    document.body.appendChild(container);

    const widgetId = window.hcaptcha.render(container, {
        sitekey: '%s',
        size: 'invisible',
        callback: (token) => { window.__capToken = token; },
        'error-callback': (err) => { window.__capError = String(err); },
        'open-callback': () => { window.__capChallengeOpen = true; },
        'close-callback': () => {},
        'expired-callback': () => { window.__capError = 'expired'; },
    });

    Promise.resolve(window.hcaptcha.execute(widgetId)).catch(() => {});
}
""" % HCAPTCHA_SITEKEY


def get_hcaptcha_token(headless: bool) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        page.goto(SITE_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_function(
            "() => typeof window.hcaptcha !== 'undefined'", timeout=60000
        )

        challenge_hint_shown = False
        page.evaluate(SETUP_CAPTCHA_JS)
        print("Solving hCaptcha...")

        deadline = time.time() + TOKEN_TIMEOUT_S
        while time.time() < deadline:
            if page.evaluate("window.__capToken"):
                break
            error = page.evaluate("window.__capError")
            if error:
                browser.close()
                raise RuntimeError(f"hCaptcha error: {error}")
            if not challenge_hint_shown and page.evaluate(
                "window.__capChallengeOpen"
            ):
                challenge_hint_shown = True
                mode = "in the browser window" if not headless else "(headless)"
                print(f">>> Captcha challenge triggered {mode}: please prove you are human.")
            time.sleep(1)
        else:
            browser.close()
            raise TimeoutError("hCaptcha token did not arrive within the timeout.")

        token = page.evaluate("window.__capToken")
        browser.close()
        return token


def generate_tts(hcaptcha_token: str) -> None:
    payload = {
        "hcaptcha_token": hcaptcha_token,
        "language_code": "kk",
        "model_id": "eleven_v3",
        "text": TEXT,
        "voice_settings": {
            "speed": 1.0,
            "stability": 0.5,
        },
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://elevenlabs.io",
        "Referer": "https://elevenlabs.io/",
        "User-Agent": "Mozilla/5.0",
    }

    with requests.post(
        TTS_URL,
        json=payload,
        headers=headers,
        stream=True,
        timeout=90,
    ) as response:
        response.raise_for_status()
        chunks = 0
        with OUTPUT_FILE.open("wb") as audio_file:
            for raw_line in response.iter_lines(decode_unicode=True):
                if not raw_line:
                    continue
                try:
                    item = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue
                audio_b64 = item.get("audio_base64")
                if audio_b64:
                    audio_file.write(base64.b64decode(audio_b64))
                    chunks += 1

    if chunks == 0:
        raise RuntimeError("No audio chunks were returned; the token or endpoint may be invalid.")
    print(f"Done: {OUTPUT_FILE} ({chunks} chunks)")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    headless = "--headless" in sys.argv
    try:
        print(f"Getting token ({'headless' if headless else 'opening browser window'})...")
        token = get_hcaptcha_token(headless=headless)
    except (PlaywrightTimeoutError, TimeoutError) as exc:
        raise SystemExit(f"Failed to get token: {exc}")
    print("Token received, sending TTS request...")
    generate_tts(token)


if __name__ == "__main__":
    main()
