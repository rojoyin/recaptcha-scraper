import logging

from fastapi import APIRouter, Depends

from scraper.schemas.scrape_response import ScrapeResponse
from scraper.schemas.url import UrlModel
from scraper.services.scraping.scraper import Scraper
from scraper.services.scraping.service_selector import get_scraper

router = APIRouter()
LOG = logging.getLogger(__name__)


@router.post("/scrape/")
async def scrape_url(item: UrlModel, scraper: Scraper = Depends(get_scraper)) -> ScrapeResponse:
    url = str(item.url)
    return await scraper.scrape(url)

