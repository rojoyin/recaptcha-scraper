from fastapi import Depends
from speech_recognition import Recognizer

from scraper.services.scraping.interfaces.challenge_solver import ChallengeSolver
from scraper.services.scraping.recaptcha_solver import ReCaptchaSolver
from scraper.services.scraping.safeguarded_scraper import SafeguardedSiteScraper
from scraper.services.scraping.interfaces.scraper import Scraper


async def get_solver() -> ChallengeSolver:
    recognizer = Recognizer()
    return ReCaptchaSolver(recognizer)


async def get_scraper(solver: ChallengeSolver = Depends(get_solver)) -> Scraper:
    return SafeguardedSiteScraper(solver)
