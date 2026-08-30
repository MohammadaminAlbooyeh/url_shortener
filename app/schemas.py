from datetime import datetime

from pydantic import BaseModel, HttpUrl, computed_field

from .config import settings


class URLBase(BaseModel):
    long_url: HttpUrl


class URLCreate(URLBase):
    pass


class URLInfo(URLBase):
    id: int
    short_code: str
    created_at: datetime
    clicks: int

    model_config = {"from_attributes": True}

    @computed_field
    @property
    def short_url(self) -> str:
        return f"{settings.base_url.rstrip('/')}/{self.short_code}"
