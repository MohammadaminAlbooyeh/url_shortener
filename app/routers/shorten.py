from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter()


@router.post("/shorten", response_model=schemas.URLInfo, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: schemas.URLCreate, db: Session = Depends(get_db)):
    return crud.create_url(db, str(payload.long_url))


@router.get("/shorten/{short_code}", response_model=schemas.URLInfo)
def get_url_info(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_by_code(db, short_code)
    if db_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    return db_url
