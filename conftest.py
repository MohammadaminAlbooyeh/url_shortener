import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

# Run tests against a dedicated test database so we never clobber the
# Alembic-managed development database.
os.environ["DATABASE_URL"] = "postgresql://amin@localhost:5432/url_shortener_test"

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402
