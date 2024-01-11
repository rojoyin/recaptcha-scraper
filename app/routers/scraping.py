from typing import Dict

from fastapi import APIRouter, HTTPException

from app.schemas.url import UrlModel
from app.services.playwright import scrape_with_playwright_async

router = APIRouter()


@router.post("/scrape/")
async def scrape_url(item: UrlModel) -> Dict[str, str]:
    try:
        url = str(item.url)
        content = await scrape_with_playwright_async(url)
        return {"data": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
