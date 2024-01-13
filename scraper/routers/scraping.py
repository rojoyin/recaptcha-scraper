import logging
from typing import Dict

from fastapi import APIRouter, HTTPException

from scraper.schemas.url import UrlModel
from scraper.services.playwright import scrape_with_playwright_async

router = APIRouter()
LOG = logging.getLogger(__name__)


@router.post("/scrape/")
async def scrape_url(item: UrlModel) -> Dict[str, str]:
    try:
        url = str(item.url)
        LOG.info(f"Receive URL to scrape: {url}")
        content = await scrape_with_playwright_async(url)
        return {"data": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
