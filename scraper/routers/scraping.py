import logging

from fastapi import APIRouter, HTTPException

from scraper.schemas.scrape_response import ScrapeResponse
from scraper.schemas.url import UrlModel
from scraper.services.playwright import scrape_with_playwright_async

router = APIRouter()
LOG = logging.getLogger(__name__)


@router.post("/scrape/")
async def scrape_url(item: UrlModel) -> ScrapeResponse:
    try:
        url = str(item.url)
        LOG.info(f"Receive URL to scrape: {url}")
        content = await scrape_with_playwright_async(url)
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
