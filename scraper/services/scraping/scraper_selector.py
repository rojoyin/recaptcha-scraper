from speech_recognition import Recognizer

from scraper.services.scraping.recaptcha_solver import ReCaptchaSolver
from scraper.services.scraping.safeguarded import SafeguardedSiteScraper
from scraper.services.scraping.scraper import Scraper


async def get_scraper() -> Scraper:
    recognizer = Recognizer()
    recaptcha_solver = ReCaptchaSolver(recognizer)
    return SafeguardedSiteScraper(recaptcha_solver)
