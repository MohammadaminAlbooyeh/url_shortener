from datetime import datetime

from pydantic import BaseModel, HttpUrl, computed_field, field_validator

from .config import settings


class URLBase(BaseModel):
    long_url: HttpUrl

    @field_validator("long_url")
    @classmethod
    def check_length(cls, value: HttpUrl) -> HttpUrl:
        if len(str(value)) > settings.max_long_url_length:
            raise ValueError(f"long_url must be at most {settings.max_long_url_length} characters")
        return value


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
