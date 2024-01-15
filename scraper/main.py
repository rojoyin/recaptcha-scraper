import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from scraper.routers import scraping

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()
app.include_router(scraping.router)

load_dotenv()


@app.get("/")
async def read_main():
    return {"message": "Hello World"}
