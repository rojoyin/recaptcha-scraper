from fastapi import Depends

from scraper.services.challenge_solver import get_solver
from scraper.services.challenge_solver.interfaces.challenge_solver import ChallengeSolver
from scraper.services.scraping.interfaces.scraper import Scraper
from scraper.services.scraping.safeguarded_scraper import SafeguardedSiteScraper


async def get_scraper(solver: ChallengeSolver = Depends(get_solver)) -> Scraper:
    return SafeguardedSiteScraper(solver)
