import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

# Run tests against a dedicated test database so we never clobber the
# Alembic-managed development database. TEST_DATABASE_URL lets CI point this
# at its own Postgres service instead of the local "amin" superuser.
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL", "postgresql://amin@localhost:5432/url_shortener_test"
)

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402
