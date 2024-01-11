from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_main():
    return {"message": "Hello World"}
