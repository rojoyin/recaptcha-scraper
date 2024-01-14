from pydantic import BaseModel


class ScrapeResponse(BaseModel):
    data: str
