import logging
import os
import random
import urllib
from tempfile import NamedTemporaryFile

import pydub
from playwright.async_api import async_playwright
from speech_recognition import AudioFile

LOG = logging.getLogger(__name__)


class ReCaptchaSolver:

    def __init__(self, recognizer):
        self.recognizer = recognizer
        self.browser = None
        self.page = None
        self.challenge_frame = None
        self.service_provider = "www.google.com"

    async def __open_browser(self, p):
        use_headless = os.getenv("headless_browser", "True") == "True"
        self.browser = await p.chromium.launch(headless=use_headless)

    async def __close_browser(self):
        if self.browser:
            await self.browser.close()

    async def __setup_page(self, url):
        LOG.info("Navigating to URL")
        self.page = await self.browser.new_page()
        await self.page.goto(url)

    def __convert_speech_to_text(self, mp3_file):
        try:
            with NamedTemporaryFile(suffix=".wav") as temp_wav_file:
                LOG.info("Transforming mp3 to wav")
                pydub.AudioSegment.from_mp3(mp3_file).export(temp_wav_file.name, format="wav")
                with AudioFile(temp_wav_file.name) as recaptcha_audio:
                    LOG.info("Transforming wav to text")
                    audio = self.recognizer.record(recaptcha_audio)
                text = self.recognizer.recognize_google(audio)
                LOG.info(f"Recognized text: {text}")
                return text
        except Exception as e:
            LOG.error("Error while processing audio: %s", e)

    async def __random_delay(self):
        waiting_time = 1000 * random.randint(1, 3)
        LOG.info(f"Waiting for {waiting_time} milliseconds")
        await self.page.wait_for_timeout(waiting_time)

    async def clean_up(self):
        LOG.info("Remove intermediate files")
        await self.__close_browser()

    async def solve(self, url):
        async with async_playwright() as p:
            try:
                await self.__open_browser(p)
                await self.__setup_page(url)
                LOG.info("Trying to solve the captcha")
                await self.__click_recaptcha_main_frame()
                await self.__click_challenge_frame()
                text = await self.__get_challenge_text()
                await self.__write_text_to_box(text)
                LOG.info("Submitting details")
                await self.page.locator('[type="submit"]').click()
                content = await self.page.content()
                return content
            except Exception as ex:
                raise Exception("Error while solving the captcha", ex)
            finally:
                await self.clean_up()

    async def __write_text_to_box(self, text):
        await self.challenge_frame.fill("id=audio-response", text)
        await self.challenge_frame.click("id=recaptcha-verify-button")
        await self.__random_delay()

    async def __get_challenge_text(self):
        href = await self.challenge_frame.locator("//a[@class='rc-audiochallenge-tdownload-link']").get_attribute(
            "href")
        parsed_url = urllib.parse.urlparse(href)

        if not self.__is_secure_url(parsed_url):
            raise Exception("Audio file insecure")

        with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3_file:
            urllib.request.urlretrieve(href, temp_mp3_file.name)
            text = self.__convert_speech_to_text(temp_mp3_file)
            return text

    def __is_secure_url(self, aux):
        return aux.scheme in ["http", "https"] and aux.netloc == self.service_provider

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
