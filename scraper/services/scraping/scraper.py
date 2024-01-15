from typing import Protocol

from scraper.schemas.scrape_response import ScrapeResponse


class Scraper(Protocol):
    async def scrape(self, url) -> ScrapeResponse:
        """
        Methdo to scrape a URL
        :param url: String with the target URL to scrape
        :return: the scraped content of the URL
        """
        pass
