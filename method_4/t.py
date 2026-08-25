import base64
import json
from playwright.sync_api import sync_playwright

TARGET_URL = "https://elevenlabs.io"
TEXT_TO_SPEAK = "Елдорияның ежелгі елінде, аспаны жарқырап, ормандары желге құпияларын сыбырлаған жерде, Зефирос атты айдаһар өмір сүрді. [sarcastically] Ол «бәрін өртеп жіберетін» түрі емес... [giggles] бірақ ол жұмсақ, дана, көздері ескі жұлдыздар сияқты еді."
OUTPUT_FILE = "output_v3_success.mp3"


def run_tts():
    with sync_playwright() as p:
        print("🚀 Браузер іске қосылуда...")
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print(f"🌐 {TARGET_URL} бетіне өтуде...")
        page.goto(TARGET_URL, wait_until="networkidle")

        # Куки баннері болса жабу
        try:
            cookie_btn = page.locator("#CookiebotDialogOkButton, button:has-text('Accept'), button:has-text('Allow all')").first
            if cookie_btn.is_visible(timeout=3000):
                cookie_btn.click()
        except Exception:
            pass

        # 1. Жоғарғы басты Omnibox виджетін табу
        print("🔍 Негізгі виджет табылуда...")
        omnibox = page.locator(".omnibox-wrapper").first
        omnibox.scroll_into_view_if_needed()

        # 2. Мәтін енгізу өрісін тазалап, жаңа мәтін жазу
        textarea = omnibox.locator("textarea").first
        textarea.wait_for(state="visible", timeout=10000)
        textarea.click()
        textarea.fill("")  # тазалау
        textarea.fill(TEXT_TO_SPEAK)
        print("✍️ Мәтін сәтті енгізілді.")

        # 3. Play батырмасын басып, келетін ағынды жауапты күту
        print("▶️ Play батырмасы басылып, жауап күтілуде...")
        play_btn = omnibox.locator("button:has-text('Play'), button[aria-label='Play']").first
        
        # Сұранысты қағып алу
        with page.expect_response(
            lambda res: ("stream" in res.url or "anonymous" in res.url) and res.status == 200,
            timeout=60000
        ) as response_info:
            play_btn.click()
            
        response = response_info.value
        print("📡 Жауап алынды, аудио жинақталуда...")

        # Ағынды жауаптың барлық байттарын оқу
        raw_body = response.body().decode("utf-8", errors="ignore")
        
        audio_chunks = []
        for line in raw_body.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if "audio_base64" in data and data["audio_base64"]:
                    audio_chunks.append(base64.b64decode(data["audio_base64"]))
            except json.JSONDecodeError:
                continue

        # 4. Файлды сақтау
        if audio_chunks:
            with open(OUTPUT_FILE, "wb") as f:
                for chunk in audio_chunks:
                    f.write(chunk)
            print(f"🎉 Аудио файл сәтті жасалды: {OUTPUT_FILE} ({len(audio_chunks)} бөлік біріктірілді)!")
        else:
            print("❌ Аудио бөліктері табылмады.")

        browser.close()
        print("🔒 Браузер жабылды.")


if __name__ == "__main__":
    run_tts()