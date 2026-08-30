import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.database import Base, engine
from app.main import app


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


def test_shorten_returns_full_short_url(client):
    resp = client.post("/shorten", json={"long_url": "https://example.com/page"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["short_code"]
    assert data["short_url"] == f"{settings.base_url.rstrip('/')}/{data['short_code']}"


def test_shorten_and_redirect(client):
    resp = client.post("/shorten", json={"long_url": "https://example.com/page"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["clicks"] == 0

    redirect = client.get(f"/{data['short_code']}", follow_redirects=False)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://example.com/page"


def test_duplicate_long_url_is_idempotent(client):
    first = client.post("/shorten", json={"long_url": "https://example.com/duplicate"})
    second = client.post("/shorten", json={"long_url": "https://example.com/duplicate"})
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["short_code"] == second.json()["short_code"]


def test_redirect_increments_clicks(client):
    data = client.post("/shorten", json={"long_url": "https://example.com/x"}).json()
    client.get(f"/{data['short_code']}")
    info = client.get(f"/shorten/{data['short_code']}").json()
    assert info["clicks"] == 1


def test_shorten_info_includes_short_url(client):
    data = client.post("/shorten", json={"long_url": "https://example.com/info"}).json()
    info = client.get(f"/shorten/{data['short_code']}").json()
    assert info["short_url"].endswith(data["short_code"])


def test_unknown_code_404(client):
    resp = client.get("/nonexistent")
    assert resp.status_code == 404


def test_shorten_rejects_scheme_less_url(client):
    resp = client.post("/shorten", json={"long_url": "example.com"})
    assert resp.status_code == 422
