import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    """Provides a fresh FastAPI test client for endpoint testing."""
    with TestClient(app) as test_client:
        yield test_client