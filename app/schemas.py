from datetime import datetime

from pydantic import BaseModel, HttpUrl


class URLBase(BaseModel):
    long_url: HttpUrl


class URLCreate(URLBase):
    pass


class URLInfo(URLBase):
    id: int
    short_code: str
    short_url: str
    created_at: datetime
    clicks: int

    model_config = {"from_attributes": True}
