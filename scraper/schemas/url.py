from pydantic import HttpUrl, BaseModel


class UrlModel(BaseModel):
    url: HttpUrl
