import logging
import os
import random
import urllib

import pydub
from playwright.async_api import async_playwright
from speech_recognition import AudioFile

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

    def __init__(self, recognizer):
        self.recognizer = recognizer
        self.browser = None
        self.page = None
        self.challenge_frame = None

    async def __open_browser(self, p):
        self.browser = await p.chromium.launch(headless=False)

    async def __close_browser(self):
        if self.browser:
            await self.browser.close()

    async def __setup_page(self, url):
        LOG.info("Navigating to URL")
        self.page = await self.browser.new_page()
        await self.page.goto(url)

    def __convert_speech_to_text(self, mp3_file):
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

    async def __random_delay(self):
        waiting_time = 1000 * random.randint(1, 3)
        LOG.info(f"Waiting for {waiting_time} milliseconds")
        await self.page.wait_for_timeout(waiting_time)

    async def solve(self, url):
        async with async_playwright() as p:
            try:
                await self.__open_browser(p)
                await self.__setup_page(url)
                LOG.info("Trying to solve the captcha")
                await self.__click_recaptcha_main_frame()
                await self.__click_challenge_frame()
                await self.__get_audio_challenge(TEMP_MP3_FILE)
                text = self.__convert_speech_to_text(TEMP_MP3_FILE)
                await self.__write_text_to_box(text)
                LOG.info("Submitting details")
                await self.page.locator('[type="submit"]').click()
                content = await self.page.content()
                await self.__close_browser()
                return content
            finally:
                await clean_up()

    async def __write_text_to_box(self, text):
        await self.challenge_frame.fill("id=audio-response", text)
        await self.challenge_frame.click("id=recaptcha-verify-button")
        await self.__random_delay()

    async def __get_audio_challenge(self, mp3_file):
        href = await self.challenge_frame.locator("//a[@class='rc-audiochallenge-tdownload-link']").get_attribute(
            "href")
        urllib.request.urlretrieve(href, mp3_file)

    async def __click_challenge_frame(self):
        challenge_frame_name = await self.page.locator(
            "//iframe[contains(@src,'https://www.google.com/recaptcha/api2/bframe?')]").get_attribute(
            "name")
        self.challenge_frame = self.page.frame(name=challenge_frame_name)
        await self.challenge_frame.click("id=recaptcha-audio-button")
        await self.challenge_frame.click("//button[@aria-labelledby='audio-instructions rc-response-label']")

    async def __click_recaptcha_main_frame(self):
        LOG.info("Find and click recaptcha iframe")
        recaptcha_frame_name = await self.page.locator("//iframe[@title='reCAPTCHA']").get_attribute("name")
        captcha = self.page.frame(name=recaptcha_frame_name)
        await captcha.click("//div[@class='recaptcha-checkbox-border']")
        await self.__random_delay()
