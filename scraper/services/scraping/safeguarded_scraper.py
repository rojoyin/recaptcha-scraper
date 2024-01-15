from scraper.schemas.scrape_response import ScrapeResponse
from scraper.services.challenge_solver.interfaces.challenge_solver import ChallengeSolver


class SafeguardedSiteScraper:

    def __init__(self, recaptcha_solver: ChallengeSolver):
        self.challenge_solver = recaptcha_solver

    async def scrape(self, url) -> ScrapeResponse:
        content = await self.challenge_solver.solve(url)
        return ScrapeResponse(data=content)
