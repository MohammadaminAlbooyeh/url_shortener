from sqlalchemy.orm import Session

from . import models, shortener


def get_by_code(db: Session, code: str) -> models.URL | None:
    return db.query(models.URL).filter(models.URL.short_code == code).first()


def get_by_long_url(db: Session, long_url: str) -> models.URL | None:
    return db.query(models.URL).filter(models.URL.long_url == long_url).first()


def create_url(db: Session, long_url: str) -> models.URL:
    existing = get_by_long_url(db, long_url)
    if existing is not None:
        return existing

    db_url = models.URL(long_url=long_url)
    db.add(db_url)
    db.flush()
    db_url.short_code = shortener.encode_base62(db_url.id)
    db.commit()
    db.refresh(db_url)
    return db_url


def increment_clicks(db: Session, db_url: models.URL) -> models.URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url
