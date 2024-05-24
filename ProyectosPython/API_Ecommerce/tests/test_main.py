import pytest
import requests
from pymongo import MongoClient
from fastapi.testclient import TestClient
from ..main import app
from config import settings


# $env:PYTHONPATH = "."; pytest -v -s # Utilizo esta linea al comienzo para darle el path a la terminal y que pytest funcione bien


# ENDPOINT = "http://127.0.0.1:8000"

# response = requests.get(ENDPOINT)
# print(response)

# data = response.json()
# print(data)
# status_code = response.status_code
# print(status_code)


# client = TestClient(app)

# @pytest.fixture(scope="module")
# def test_app():
#     client = TestClient(app)
#     yield client

# @pytest.fixture(scope="module")
# def db_client():
#     client = MongoClient()
#     yield client

# @pytest.fixture(scope="function", autouse=True)
# def clear_db(db_client):
#     db_client.get_database("local").drop_collection("test_users")
#     print("Eliminamos coleccion test")


# Testeamos la raíz de la web.
@pytest.mark.usefixtures("test_app")
def test_read_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == "Bienvenido a Fakebook Marketplace"
    

# Testeamos el registro de un usuario
@pytest.mark.usefixtures("test_app")
def test_register_user(test_app):
    user_data = {
        "username": "test_username",
        "email": "test@email.com",
        "firstname": "Agu",
        "lastname": "Uga",
        "dateofbirth": "1994-01-28",
        "country": "Arg",
        "city": "BsAs",
        "password": "nico"
    }
    response = test_app.post("/register", json=user_data)
    # print(response.json())
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == "test_username"
    

