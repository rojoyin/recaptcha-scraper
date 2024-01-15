from typing import Any

from scraper.services.scraping.challenge_solver import ChallengeSolver


class SafeguardedSiteScraper:

    def __init__(self, recaptcha_solver: ChallengeSolver):
        self.challenge_solver = recaptcha_solver

    async def scrape(self, url) -> dict[str, Any]:
        content = await self.challenge_solver.solve(url)
        return {"data": content}
