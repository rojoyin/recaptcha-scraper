import logging
import random
import urllib.request

import pydub
from playwright.async_api import async_playwright
from speech_recognition import AudioFile, Recognizer


LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


async def scrape_with_playwright_async(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        name = await page.locator("//iframe[@title='reCAPTCHA']").get_attribute("name")
        captcha = page.frame(name=name)
        await captcha.click("//div[@class='recaptcha-checkbox-border']")
        await page.wait_for_timeout(random.randint(1, 3) * 1000)
        name_ = await page.locator(
            "//iframe[contains(@src,'https://www.google.com/recaptcha/api2/bframe?')]").get_attribute(
            "name")
        main_frame = page.frame(name=name_)
        await main_frame.click("id=recaptcha-audio-button")
        await main_frame.click("//button[@aria-labelledby='audio-instructions rc-response-label']")
        href = await main_frame.locator("//a[@class='rc-audiochallenge-tdownload-link']").get_attribute("href")
        urllib.request.urlretrieve(href, "audio.mp3")
        pydub.AudioSegment.from_mp3("audio.mp3").export("audio.wav", format="wav")
        recognizer = Recognizer()
        recaptcha_audio = AudioFile("audio.wav")
        with recaptcha_audio as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)
        LOG.info(f"Recognized text: {text}")
        await main_frame.fill("id=audio-response", text)
        await main_frame.click("id=recaptcha-verify-button")
        await page.wait_for_timeout(1000 * random.randint(1, 3))
        submit_button = page.locator('[type="submit"]')
        await submit_button.click()
        await page.wait_for_timeout(1000 * random.randint(1, 3))
        content = await page.content()
        await browser.close()
        return content
