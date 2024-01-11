from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl

router = APIRouter()


class UrlModel(BaseModel):
    url: HttpUrl


@router.post("/scrape/")
async def scrape_url(target_url: UrlModel):
    return {"url": target_url, "content": "Scraped content"}
