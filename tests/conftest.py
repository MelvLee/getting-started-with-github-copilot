import copy

import pytest
from fastapi.testclient import TestClient

from src import app as src_app
from src.app import app


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict before/after each test."""
    original = copy.deepcopy(src_app.activities)
    yield
    src_app.activities.clear()
    src_app.activities.update(original)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
