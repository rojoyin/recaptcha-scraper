from fastapi import FastAPI

from app.routers import scraping

app = FastAPI()
app.include_router(scraping.router)


@app.get("/")
async def read_main():
    return {"message": "Hello World"}
