import os
from pathlib import Path
DB=Path("/tmp/pocketsmart_test.db")
if DB.exists(): DB.unlink()
os.environ["DATABASE_URL"]=f"sqlite:///{DB}"
os.environ["SECRET_KEY"]="test-secret"
os.environ["GEMINI_API_KEY"]=""
import pytest
from fastapi.testclient import TestClient
from app.database import init_db
from app.main import app
@pytest.fixture(scope="session")
def client():
    init_db()
    with TestClient(app) as c: yield c
