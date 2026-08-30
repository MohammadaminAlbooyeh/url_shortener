from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, func

from .database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_code = Column(String(10), unique=True, index=True, nullable=True)
    long_url = Column(String(2048), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    clicks = Column(Integer, default=0, nullable=False)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "short_code": self.short_code,
            "long_url": self.long_url,
            "created_at": self.created_at,
            "clicks": self.clicks,
        }
