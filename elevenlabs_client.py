import os
import time
import re
import datetime
from playwright.sync_api import sync_playwright, expect, Page, TimeoutError

def info(msg: str):
    """Logs an informational message."""
    print(f"[INFO] {datetime.datetime.now().isoformat()} | {msg}")

def error(msg: str):
    """Logs an error message."""
    print(f"[ERROR] {datetime.datetime.now().isoformat()} | {msg}")

class ElevenLabsClient:
    """
    A Playwright-based client to automate interactions with the ElevenLabs website,
    relying solely on a persistent user data directory for session management.
    """
    BASE_URL = "https://elevenlabs.io"
    SPEECH_SYNTHESIS_URL = f"{BASE_URL}/app/speech-synthesis"

    def __init__(self, email: str, password: str, user_data_dir="user_data_dir"):
        if not email or not password:
            error("EMAIL and PASSWORD must be set!")
            raise ValueError("Email and password cannot be empty.")
        self.email = email
        self.password = password
        self.user_data_dir = user_data_dir
        self.playwright = None
        self.browser = None
        self.page = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        info("Browser closed successfully. Session saved to persistent directory.")

    def launch(self, headless=True) -> Page:
        launch_args = ["--disable-blink-features=AutomationControlled"]
        context_args = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "viewport": {"width": 1280, "height": 720},
            "headless": headless,
            "args": launch_args,
        }
        info(f"Launching persistent context with user_data_dir='{self.user_data_dir}'...")
        self.browser = self.playwright.chromium.launch_persistent_context(self.user_data_dir, **context_args)
        self.page = self.browser.pages[0] if self.browser.pages else self.browser.new_page()
        self.page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        info(f"Navigating to {self.SPEECH_SYNTHESIS_URL} to check login status...")
        self.page.goto(self.SPEECH_SYNTHESIS_URL)
        try:
            expect(self.page.get_by_role('heading', name='Text to Speech')).to_be_visible(timeout=15000)
            info("✅ Already logged in using persistent profile.")
        except TimeoutError:
            info("Session not found or expired. Logging in is required.")
            self._login()
            self.page.goto(self.SPEECH_SYNTHESIS_URL)
            expect(self.page.get_by_role('heading', name='Text to Speech')).to_be_visible(timeout=20000)
        self._handle_initial_dialogs()
        return self.page

    def _login(self):
        LOGIN_URL = f"{self.BASE_URL}/app/sign-in"
        info(f"Navigating to {LOGIN_URL}")
        self.page.goto(LOGIN_URL)
        self.page.get_by_placeholder("Enter your email address").fill(self.email)
        self.page.get_by_placeholder("Enter your password").fill(self.password)
        self.page.locator('[data-testid="sign-in-submit-button"]').click()
        info("Waiting for login result (success or error)...")
        error_selector = '[data-sonner-toast][data-type="error"]'
        try:
            self.page.wait_for_url(f"{self.BASE_URL}/app/**", timeout=15000)
            info("✅ Login successful!")
        except TimeoutError:
            if self.page.locator(error_selector).is_visible():
                error_message = self.page.locator(error_selector).inner_text()
                raise Exception(f"Login Failed! Reason from website: {error_message}")
            else:
                self.page.screenshot(path="login_unexpected_error.png")
                raise Exception("Login failed for an unknown reason. A screenshot was saved.")

    def _handle_initial_dialogs(self):
        info("Checking for any initial dialogs...")
        try:
            get_started_button = self.page.locator('[data-testid="v3-welcome-dialog-get-started"]')
            info("Checking for 'What's new' dialog...")
            get_started_button.click(timeout=7000)
            info("💡 'What's new' dialog found and closed.")
        except TimeoutError:
            info("✅ 'What's new' dialog did not appear, which is normal.")
        except Exception as e:
            error(f"An error occurred while trying to close the 'What's new' dialog: {e}")
        try:
            accept_cookies_button = self.page.get_by_role('button', name=re.compile(r'Accept all|Allow all', re.IGNORECASE))
            accept_cookies_button.click(timeout=5000)
            info("🍪 Cookie banner found and accepted.")
        except TimeoutError:
            info("✅ Cookie banner did not appear.")
        except Exception as e:
            error(f"Could not close cookie banner: {e}")

    def scrape_voices(self):
        info("Scraping voice list...")
        voice_dropdown_button = self.page.get_by_label(re.compile(r"Select voice", re.IGNORECASE))
        expect(voice_dropdown_button).to_be_visible()
        voice_dropdown_button.click()
        voice_dialog = self.page.locator('[role="dialog"]:has-text("Select a voice")')
        expect(voice_dialog).to_be_visible()
        voices = []
        for item in voice_dialog.locator('li.eleven-list-item').all():
            try:
                name = item.locator('p > span.truncate').inner_text().strip()
                if name:
                    voices.append(name)
            except Exception:
                continue
        self.page.keyboard.press("Escape")
        info(f"Voices found: {voices}")
        return voices

    def select_voice(self, voice_name: str):
        info(f"Selecting voice: '{voice_name}'")
        self.page.get_by_label(re.compile(r"Select voice", re.IGNORECASE)).click()
        voice_dialog = self.page.locator('[role="dialog"]:has-text("Select a voice")')
        expect(voice_dialog).to_be_visible()
        search_input = voice_dialog.get_by_placeholder("Search voices...")
        search_input.fill(voice_name)
        time.sleep(1)
        # Wait for at least one result to appear
        voice_items = voice_dialog.locator('li.eleven-list-item')
        expect(voice_items.first).to_be_visible(timeout=10000)
        first_voice = voice_items.first
        selected_name = first_voice.locator('p > span.truncate').inner_text().strip()
        first_voice.click()
        expect(voice_dialog).not_to_be_visible()
        info(f"✅ Voice '{selected_name}' selected successfully.")

    def generate_and_download(self, voice_name: str, text: str):
        """
        Synthesizes speech and downloads the two generated options ('Generation 1' and 'Generation 2')
        into the specified output paths.
        """
        self.select_voice(voice_name)
        info("Filling text into the editor...")
        self.page.locator('div.tiptap.ProseMirror').fill(text)
        generate_button = self.page.get_by_role('button', name='Generate speech')
        expect(generate_button).to_be_enabled()
        generate_button.click()
        info("Waiting for the two generation options to appear...")
        generation_container = self.page.locator('div.grid:has-text("Which generation do you prefer?")')
        try:
            expect(generation_container).to_be_visible(timeout=90000)
            info("✅ 'Which generation do you prefer?' container is visible.")
        except TimeoutError:
            error("The two generation options did not appear in time. This might happen if the feature is A/B tested or disabled.")
            self.page.screenshot(path="generation_options_timeout.png")
            raise
        gen1_block = generation_container.locator('div:has(> p:text-is("Generation 1"))')
        gen2_block = generation_container.locator('div:has(> p:text-is("Generation 2"))')
        info("Locating 'Generation 1' and its download button...")
        expect(gen1_block).to_be_visible()
        download_btn_1 = gen1_block.get_by_label("Download")
        expect(download_btn_1).to_be_visible()
        output_path1 = "output1.mp3"
        with self.page.expect_download() as download1_info:
            download_btn_1.click()
            info(f"Downloading Generation 1 to {output_path1}...")
        download1 = download1_info.value
        download1.save_as(output_path1)
        info(f"✅ 'Generation 1' downloaded successfully to: {output_path1}")
        info("Locating 'Generation 2' and its download button...")
        expect(gen2_block).to_be_visible()
        download_btn_2 = gen2_block.get_by_label("Download")
        expect(download_btn_2).to_be_visible()
        output_path2 = "output2.mp3"
        with self.page.expect_download() as download2_info:
            download_btn_2.click()
            info(f"Downloading Generation 2 to {output_path2}...")
        download2 = download2_info.value
        download2.save_as(output_path2)
        info(f"✅ 'Generation 2' downloaded successfully to: {output_path2}")
