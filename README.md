# URL Shortener

A small URL shortener built with FastAPI, SQLAlchemy and Alembic. Short codes are
generated with **base62 encoding of an auto-increment primary key** (`id -> base62`).

## Features

- `POST /shorten` — create a short link from a long URL
- `GET /{short_code}` — redirect to the original URL (307) and count a click
- `GET /shorten/{short_code}` — fetch info about a short link (click count, etc.)
- Base62 short codes derived from an auto-incrementing integer `id`
- Alembic migrations, Pydantic settings from env, SQLite by default

## Project layout

```
url_shortener/
├── app/
│   ├── main.py          # FastAPI app + routers
│   ├── config.py        # settings (env: DATABASE_URL, BASE_URL)
│   ├── database.py      # engine / session / Base / get_db
│   ├── models.py        # URL ORM model
│   ├── schemas.py       # Pydantic request/response
│   ├── crud.py          # DB operations
│   ├── shortener.py     # base62 encode/decode
│   └── routers/         # shorten.py, redirect.py
├── alembic/             # migrations
├── tests/               # pytest tests
└── .env.example
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
uvicorn app.main:app --reload
```

Then open http://localhost:8000/docs for the interactive API docs.

Create a short link:

```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://example.com/some/long/path"}'
```

## Database / migrations

Tables are auto-created on startup via `Base.metadata.create_all`. For managed
migrations use Alembic:

```bash
alembic revision --autogenerate -m "create urls table"
alembic upgrade head
```

## Tests

```bash
pytest
```
