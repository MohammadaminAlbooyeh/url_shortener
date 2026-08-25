from sqlalchemy.orm import Session

from . import models, shortener


def create_url(db: Session, long_url: str) -> models.URL:
    db_url = models.URL(long_url=long_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    db_url.short_code = shortener.encode_base62(db_url.id)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_by_code(db: Session, code: str) -> models.URL | None:
    return db.query(models.URL).filter(models.URL.short_code == code).first()


def increment_clicks(db: Session, db_url: models.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url
