from typing import Protocol, Any


class Scraper(Protocol):
    async def scrape(self, url) -> dict[str, Any]:
        """
        Methdo to scrape a URL
        :param url: String with the target URL to scrape
        :return: the scraped content of the URL
        """
        pass
