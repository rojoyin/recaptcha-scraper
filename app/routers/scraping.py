from fastapi import APIRouter

from app.schemas.url import UrlModel

router = APIRouter()


@router.post("/scrape/")
async def scrape_url(target_url: UrlModel):
    return {"url": target_url, "content": "Scraped content"}
