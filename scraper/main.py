import logging

from fastapi import FastAPI

from scraper.routers import scraping

app = FastAPI()
app.include_router(scraping.router)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@app.get("/")
async def read_main():
    return {"message": "Hello World"}
