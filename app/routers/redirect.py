from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .. import crud
from ..database import get_db

router = APIRouter()


@router.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_by_code(db, short_code)
    if db_url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")

    crud.increment_clicks(db, db_url)
    return RedirectResponse(db_url.long_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
