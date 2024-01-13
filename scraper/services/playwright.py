import logging
import os
import random
import urllib.request

import pydub
from playwright.async_api import async_playwright
from speech_recognition import AudioFile, Recognizer

LOG = logging.getLogger(__name__)
TEMP_MP3_FILE = "audio.mp3"
TEMP_WAV_FILE = "audio.wav"


async def clean_up():
    LOG.info("Remove intermediate files")
    if os.path.exists(TEMP_MP3_FILE):
        os.remove(TEMP_MP3_FILE)
    if os.path.exists(TEMP_WAV_FILE):
        os.remove(TEMP_WAV_FILE)


class ReCaptchaSolver:

    def __init__(self, playwright, url):
        self.recognizer = Recognizer()
        self.playwright = playwright
        self.url = url
        self.browser = None
        self.page = None
        LOG.info("Created solver class")

    async def setup_page(self):
        LOG.info("Navigating to URL")
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        await self.page.goto(self.url)

    def convert_speech_to_text(self, mp3_file):
        try:
            LOG.info("Downloading audio")
            pydub.AudioSegment.from_mp3(mp3_file).export(TEMP_WAV_FILE, format="wav")
            recaptcha_audio = AudioFile(TEMP_WAV_FILE)
            LOG.info("Converting audio to text")
            with recaptcha_audio as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio)
            LOG.info(f"Recognized text: {text}")
            return text
        except Exception as e:
            LOG.error("Error while processing audio", e)

    async def random_delay(self):
        waiting_time = 1000 * random.randint(1, 3)
        LOG.info(f"Waiting for {waiting_time} milliseconds")
        await self.page.wait_for_timeout(random.randint(1, 3) * 1000)

    async def solve(self):
        LOG.info("Attempting to solve the captcha")

        # find the recaptcha iframe
        recaptcha_frame_name = await self.page.locator("//iframe[@title='reCAPTCHA']").get_attribute("name")
        captcha = self.page.frame(name=recaptcha_frame_name)
        await captcha.click("//div[@class='recaptcha-checkbox-border']")
        await self.random_delay()

        # find the challenge iframe
        challenge_frame_name = await self.page.locator(
            "//iframe[contains(@src,'https://www.google.com/recaptcha/api2/bframe?')]").get_attribute(
            "name")
        challenge_frame = self.page.frame(name=challenge_frame_name)
        await challenge_frame.click("id=recaptcha-audio-button")
        await challenge_frame.click("//button[@aria-labelledby='audio-instructions rc-response-label']")
        href = await challenge_frame.locator("//a[@class='rc-audiochallenge-tdownload-link']").get_attribute("href")
        urllib.request.urlretrieve(href, TEMP_MP3_FILE)
        text = self.convert_speech_to_text(TEMP_MP3_FILE)
        await challenge_frame.fill("id=audio-response", text)
        await challenge_frame.click("id=recaptcha-verify-button")
        await self.random_delay()
        submit_button = self.page.locator('[type="submit"]')
        await submit_button.click()
        await self.random_delay()
        content = await self.page.content()
        return content


async def scrape_with_playwright_async(url: str):
    async with async_playwright() as p:
        try:
            solver = ReCaptchaSolver(p, url)
            await solver.setup_page()
            content = await solver.solve()
            await clean_up()
            return content
        finally:
            await clean_up()
