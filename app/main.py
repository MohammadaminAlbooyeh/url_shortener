from fastapi import FastAPI

from .database import Base, engine
from .routers import redirect, shorten

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener", version="1.0.0")

app.include_router(shorten.router)
app.include_router(redirect.router)


@app.get("/")
def root():
    return {"message": "URL Shortener API. POST to /shorten to create a short link."}
