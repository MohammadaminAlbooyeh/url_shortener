from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .database import Base, engine
from .limiter import limiter
from .routers import redirect, shorten

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(shorten.router)
app.include_router(redirect.router)


@app.get("/")
def root():
    return {"message": "URL Shortener API. POST to /shorten to create a short link."}
