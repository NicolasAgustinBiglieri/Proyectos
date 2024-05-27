import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from ..main import app

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client

@pytest.fixture(scope="module")
def db_client():
    client = MongoClient()
    yield client

@pytest.fixture(scope="function", autouse=True)
def clear_db(db_client):
    db_client.get_database("local").drop_collection("test_users")