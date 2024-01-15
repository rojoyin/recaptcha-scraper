from typing import Any


from scraper.services.scraping.recaptcha_solver import ReCaptchaSolver


class SafeguardedSiteScraper:

    def __init__(self, recaptcha_solver: ReCaptchaSolver):
        self.recaptcha_solver = recaptcha_solver

    async def scrape(self, url) -> dict[str, Any]:
        content = await self.recaptcha_solver.solve(url)
        return {"data": content}
