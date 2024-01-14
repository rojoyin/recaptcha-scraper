from fastapi import FastAPI

from scraper.routers import scraping

app = FastAPI()
app.include_router(scraping.router)


@app.get("/")
async def read_main():
    return {"message": "Hello World"}
